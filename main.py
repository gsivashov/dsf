import os
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
        return response
    else:
        print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
        

def print_result(response, keyword, fileds):
    # parse result and return only organic result
    data = response['tasks'][0]['result'][0]['items']
    
    result = []

    for item in data:
        item_list = [str(item[field]) for field in fields if item['type'] == 'organic']
        item_list.insert(0,keyword)
        if len(item_list) > 1:
            result.append(item_list)
    return result


def main(start_file, fields):
    print(f"keyword|{'|'.join(fields)}")
    with open(start_file) as keywords:
        for keyword in keywords:
            keyword = keyword.strip().lower()
            result = get_results(keyword)
            for row in print_result(result, keyword, fields):
                if 'anibis.ch' in row[1]:
                    print('|'.join(row))

if __name__ == '__main__':
    load_dotenv()
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    client = RestClient(login, password)
    start_file = 'keywords.txt'
    fields = ['domain', 'extended_snippet', 'faq', 'is_featured_snippet', 'rank_absolute', 'rank_group', 'type', 'url']

    main(start_file, fields)