# get_query_from_API.py collect json query from petfinder API

import json
import requests
from tqdm import tqdm

# original curl command
# : curl -d "grant_type=client_credentials&client_id={CLIENT-ID}&client_secret={CLIENT-SECRET}" https://api.petfinder.com/v2/oauth2/token
# : curl -H "Authorization: Bearer {YOUR_ACCESS_TOKEN}" GET https://api.petfinder.com/v2/{CATEGORY}/{ACTION}?{parameter_1}={value_1}&{parameter_2}={value_2}

def get_imageURL(api_key_path = './api_account.json', file_path = './meta_data.json', page_number = 995):

    with open(api_key_path, 'r', encoding='UTF-8') as f:
        json_object = json.load(f)
        api_key = json_object['petfinder']['api_key']
        api_secret = json_object['petfinder']['api_secret']

    headers_token = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data_token = {
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': api_secret
    }

    response_token = requests.post('https://api.petfinder.com/v2/oauth2/token', headers=headers_token, data=data_token)

    access_token = json.loads(response_token.text)['access_token']

    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    params = {
        'type': 'cat',
    }


    meta = {}

    with open(file_path, 'r', encoding='UTF-8') as f:
        json_object = json.load(f)
        if not json_object:
            meta['list_cat'] = []
            meta['page_last'] = 0
            print("No data in meta_data.json")
            
        else: 
            meta['list_cat']  = json_object['list_cat']
            meta['page_last'] = json_object['page_last']
            print("Total number of cats: ", len(meta['list_cat']))
            print("Last page: ", meta['page_last'])

    page_read_1st = meta['page_last'] + 1
    page_read_last = page_read_1st + page_number

    pbar = tqdm(range(page_read_1st, page_read_last))
    pbar.set_description("Collecting json data from API")
    for i in pbar:
        params['page'] = str(i)
        response = requests.get('https://api.petfinder.com/v2/animals', headers=headers, params=params)
        json_object = json.loads(response.text)

        if json_object.get('status') != None:
            if json_object['status'] == 429:
                print('\n\033[31m \033[43mError Occured:'+'\033[31m \033[44m'+json_object['detail']+ '\033[0m')
                break

        data = json_object['animals']

        for cat in data:
            for tmp in meta['list_cat']:
                if cat['id'] == tmp['id']:
                    print("Cat id: ", cat['id'], " already exists")
                    break
            if cat['photos'] != []:
                dict_cat = {}
                dict_cat['id'] = cat['id']
                dict_cat['num_photos'] = len(cat['photos'])
                dict_cat['photos'] = []
                for photo in cat['photos']:
                    dict_cat['photos'].append(photo['full'])
                meta['list_cat'].append(dict_cat)
            
        
    meta['page_last'] = (page_read_last - 1)

    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent="\t")


if __name__ == '__main__':
    get_imageURL()