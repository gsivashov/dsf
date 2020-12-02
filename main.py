import os
from client import RestClient
from dotenv import load_dotenv


load_dotenv()
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

client = RestClient(login, password)

with open('keywords.txt') as keywords:
    for keyword in keywords:
        keyword = keyword.strip().lower()

        post_data = dict()
        post_data[len(post_data)] = dict(
            language_code="de",
            location_code=2756,
            keyword=keyword,
            calculate_rectangles=True
        )
        response = client.post("/v3/serp/google/organic/live/advanced", post_data)
        if response["status_code"] == 20000:
            data = response['tasks'][0]['result'][0]['items']

            print('Keyword|Rank_Absolute|Rank_Group|Type|Domain|URL|FAQ|Extended_Snippet')

            for item in data:
                if item['type'] != 'organic':
                    continue
                else:
                    print(f"{item['rank_absolute']}|"\
                          f"{item['rank_group']}|"\
                          f"{item['type']}|"\
                          f"{item['domain']}|"\
                          f"{item['url']}|"\
                          f"{item['faq']}|"\
                          f"{item['extended_snippet']}")

        else:
            print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))