import csv
import json
import os

from client import RestClient
from dotenv import load_dotenv
from time import sleep


def create_chunk(file, size=700):
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

    for keyword in chunk:
        post_tasks[len(post_tasks)] = dict(
            language_code="de",
            location_code=2756,
            keywords=keyword,
        )
    return post_tasks


def post_tasks(tasks):

    response = client.post(
        "/v3/keywords_data/google/search_volume/task_post", tasks)

    ids = [id['id'] for id in response['tasks']]

    return ids


def get_tasks(ids):

    response = client.get("/v3/keywords_data/google/search_volume/tasks_ready")

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


def main():

    CREATE_TASK = create_tasks(create_chunk('keywords.txt'))
    POST_TASK = post_tasks(CREATE_TASK)
    sleep(20)
    GET_TASK = get_tasks(POST_TASK)

    print(json.dumps(GET_TASK, indent=4))


if __name__ == '__main__':

    load_dotenv()
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    client = RestClient(login, password)

    main()
