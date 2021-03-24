import csv
import json
import os
import argparse

from client import RestClient
from dotenv import load_dotenv
from time import sleep


def create_chunk(file, size=200):
    chunk = []
    with open(file) as file:
        reader = csv.reader(file)
        next(reader)

        for line in reader:
            if not line:
                continue

            keyword = line[0].replace('\u00e0', 'a')
            chunk.append(keyword)
            if len(chunk) % size == 0:
                yield chunk
                chunk = []
        if chunk:
            yield chunk


def create_tasks(chunk):

    post_tasks = dict()

    for categories in chunk:
        for category in categories:
            post_tasks[len(post_tasks)] = dict(
                language_code="de",
                location_code=2756,
                category_code=category,
            )
    return post_tasks


def post_tasks(tasks):

    response = client.post(
        "/v3/keywords_data/google/keywords_for_category/task_post", tasks)

    # ids = [id['id'] for id in response['tasks']]
    tasks_count = response['tasks_count']
    err = response['tasks_error']
    err_message = response['tasks'][0]['status_message']

    return tasks_count, err, err_message


def get_tasks():

    response = client.get(
        "/v3/keywords_data/google/keywords_for_category/tasks_ready")

    if response['status_code'] == 20000:
        for task in response['tasks']:
            if (task['result'] and (len(task['result']) > 0)):
                for resultTaskInfo in task['result']:
                    if(resultTaskInfo['endpoint']):
                        results = (client.get(resultTaskInfo['endpoint']))

                        data = dict()
                        for keywords_data in results['tasks']:
                            if (keywords_data['result'] and (len(keywords_data['result']) > 0)):
                                for keyword in keywords_data['result']:
                                    data[keyword['keyword']
                                         ] = keyword['search_volume']

                        return data
    else:
        print("error. Code: %d Message: %s" %
              (response["status_code"], response["status_message"]))


def print_results(result):
    for key in result:
        print(f'{key}|{result[key]}')


def main(params):

    FILE = params.file

    CREATE_TASK = create_tasks(create_chunk(FILE))
    POST_TASK = post_tasks(CREATE_TASK)
    print(POST_TASK)
    while True:
        sleep(20)
        GET_TASK = get_tasks()
        print_results(GET_TASK)
        if GET_TASK:
            break


if __name__ == '__main__':

    load_dotenv()
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    client = RestClient(login, password)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--file',
        type=str,
        default='category.txt',
        help='enter path to file wih KEYWORDS. default: keywords.txt',
    )

    params = parser.parse_args()

    main(params)
