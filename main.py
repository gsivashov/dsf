import os
import logging
import argparse

from pathlib import Path
from client import RestClient
from dotenv import load_dotenv

def get_results(keyword):
    # send request to DataForSEO and return response
    post_data = dict()
    post_data[len(post_data)] = dict(
        language_code="de",
        location_code=2756,
        keyword=keyword,
        calculate_rectangles=True
    )
    response = client.post("/v3/serp/google/organic/live/advanced", post_data)
    if response["status_code"] == 20000:
        if response['tasks'][0]['status_code'] == 20000:
            return response
        else: logging.info("error. Code: %d Message: %s" % (response['tasks'][0]['status_code'], response['tasks'][0]["status_message"]))
    else:
        logging.info("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
        

def parse_result(response, keyword, fileds, domains):
    # parse result and return only organic result
    data = response['tasks'][0]['result'][0]['items']
    
    result = []

    for item in data:
        item_list = [
            str(item[field]) for domain in domains for field in fields 
            if item['type'] == 'organic' and domain in item['domain']
        ]
        item_list.insert(0,keyword)
        if len(item_list) > 1:
            result.append(item_list)
    return result


def main(params, fields):

    keywords = Path(params.keywords)
    domains = Path(params.domains)
    # table header:
    print(f"keyword|{'|'.join(fields)}")

    # main loop for sending requests:
    with open(keywords) as keywords:
        for keyword in keywords:
            keyword = keyword.strip().lower()

            logging.info(keyword)

            try:
                result = get_results(keyword)
                for row in parse_result(result, keyword, fields, domains):
                    print('|'.join(row), flush=True)

            except Exception as e:
                error = str(e)
            if error:
                logging.error(error)
            else:
                logging.info(
                    f'{keyword} data SUCCESSFULLY collected'
                )

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
    # start_file = 'keywords.txt'

    fields = [
        'domain',
        'extended_snippet',
        'faq',
        'is_featured_snippet',
        'rank_absolute',
        'rank_group',
        'type',
        'url'
    ]
    # domains = ['www.anibis.ch']

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--domains',
        type=str,
        default='domains.txt',
        help='enter path to file with DOMAINS. default: domains.txt'
    )

    parser.add_argument(
        '--keywords',
        type=str,
        default='keywords.txt',
        help='enter path to file wih KEYWORDS. default: keywords.txt'
    )
    
    params = parser.parse_args()

    logging.info('Started')
    
    main(params, fields)

    logging.info('Done')
