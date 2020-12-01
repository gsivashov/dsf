from client import RestClient
import json

login = 'seo@geo.scout24.ch'
password = 'f54cf34a878fe078'

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
                    print(f"{keyword}|{item['rank_absolute']}|{item['rank_group']}|{item['type']}|{item['domain']}|{item['url']}|{item['faq']}|{item['extended_snippet']}")

        else:
            print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))