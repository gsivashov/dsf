import json

with open('res.json') as start_file:
    data = json.load(start_file)
    
    print('Rank_Absolute|Rank_Group|Type|Domain|URL|FAQ|Extended_Snippet')
    for item in data[0]['items']:
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
    # import pdb; pdb.set_trace()


# key - item -> rank_absolute; type; domain; url; group_rank; faq; extended_snippet
