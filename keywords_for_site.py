import csv
import json
import os
import argparse

from client import RestClient
from dotenv import load_dotenv
from time import sleep


def create_tasks(domain):

    post_tasks = dict()

    post_tasks[len(post_tasks)] = dict(
        language_code="de",
        location_code=2756,
        target=domain,
    )
    return post_tasks


def post_tasks(tasks):

    response = client.post(
        "/v3/keywords_data/google/keywords_for_site/task_post", tasks)

    # ids = [id['id'] for id in response['tasks']]
    tasks_count = response['tasks_count']
    err = response['tasks_error']
    err_message = response['tasks'][0]['status_message']

    return tasks_count, err, err_message


def get_tasks():

    response = client.get(
        "/v3/keywords_data/google/keywords_for_site/tasks_ready")

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

    DOMAIN = params.domain

    CREATE_TASK = create_tasks(DOMAIN)
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
        '--domain',
        type=str,
        default='anibis.ch',
        help='enter domain name. default: site.com',
        # required=True
    )

    params = parser.parse_args()

    main(params)
