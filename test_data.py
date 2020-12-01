import json

with open('res.json') as start_file:
    data = json.load(start_file)
    
    print('Rank_Absolute|Rank_Group|Type|Domain|URL|FAQ|Extended_Snippet')
    for item in data[0]['items']:
        if item['type'] != 'organic':
            continue
        else:
            print(f"{item['rank_absolute']}|{item['rank_group']}|{item['type']}|{item['domain']}|{item['url']}|{item['faq']}|{item['extended_snippet']}")
    # import pdb; pdb.set_trace()


# key - item -> rank_absolute; type; domain; url; group_rank; faq; extended_snippet
