import time
import os
import logging
import argparse
import csv

from pathlib import Path
from client import RestClient
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


def get_results(keyword):
    '''
    send request to DataForSEO and return response
    if error - add's message to log file
    '''

    post_data = dict()
    post_data[len(post_data)] = dict(
        language_code="de",
        location_code=2756,
        keyword=keyword,
        se_domain="google.ch",
        calculate_rectangles=True
    )
    response = client.post("/v3/serp/google/organic/live/advanced", post_data)
    # check API errors - no money or no response etc. Logging in to main.log file

    if response["status_code"] == 20000:
        if response['tasks'][0]['status_code'] == 20000:
            return response
        else:
            logging.info(
                f'error. Code: {response["tasks"][0]["status_code"]} '
                f'Message: {response["tasks"][0]["status_message"]}'
            )
    else:
        logging.info(
            f'error. Code: {response["status_code"]}'
            f'Message: {response["status_message"]}'
        )


def chunkinator(file, size, index, delimiter):
    '''
    Spilts file to chunks
    You need to pass:
    size of chunk;
    index of column with keywords;
    delimiter for columns
    '''
    chunk = []
    with open(file) as file:
        reader = csv.reader(file, delimiter=delimiter)
        next(reader)

        for line in reader:
            # line = line.strip()
            if not line:
                continue

            keyword = line[index].strip().lower()
            chunk.append(keyword)
            if len(chunk) % size == 0:
                yield chunk
                chunk = []
        if chunk:
            yield chunk


def parse_result(response, fields):
    '''
    parse result and return only organic result
    '''

    data = response['tasks'][0]['result'][0]['items']
    keyword = response['tasks'][0]['result'][0]['keyword']
    check_url = response['tasks'][0]['result'][0]['check_url']

    result = []
    for item in data:
        if item['type'] == 'organic':
            item_list = [str(item[field]) for field in fields]
            item_list.insert(0, keyword)
            item_list.append(check_url)
            if len(item_list) > 2:
                result.append(item_list)
    return result


def main(params, fields, size):

    keywords = params.keywords
    # domains = params.domains
    line_index = params.line
    delimiter = params.delimiter

    # table header:
    print(f"Keyword|{'|'.join(fields)}|Check_url")

    # main loop for sending requests:
    with ThreadPoolExecutor(max_workers=size) as executor:
        for chunk in chunkinator(keywords, size, line_index, delimiter):
            features = executor.map(get_results, chunk, chunksize=size)
            for data in features:
                result = parse_result(data, fields)
                for row in result:
                    print(f'{"|".join(row)}')


if __name__ == '__main__':

    logging.basicConfig(
        filename=Path().cwd() / 'logs' / 'main.log',
        filemode='a',
        level=logging.INFO,
        format='%(levelname)s:%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    load_dotenv()
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    client = RestClient(login, password)

    organic_fields = [
        'domain',
        'extended_snippet',
        'faq',
        'rank_group',
        'type',
        'url'
    ]

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--line',
        type=int,
        help='index of line with keywords',
        required=True
    )

    parser.add_argument(
        '--keywords',
        type=str,
        default='keywords.txt',
        help='enter path to file wih KEYWORDS. default: keywords.txt',
        required=True
    )

    parser.add_argument(
        '--domains',
        type=str,
        default='domains.txt',
        help='enter path to file with DOMAINS. default: domains.txt'
    )

    parser.add_argument(
        '--delimiter',
        type=str,
        help='csv delimiter (default "|")',
        default='|',
    )

    params = parser.parse_args()

    logging.info('Started')
    start = time.perf_counter()

    main(params, organic_fields, 5)

    end = time.perf_counter()
    print('elapsed time: ', end - start)
    logging.info('Done')
