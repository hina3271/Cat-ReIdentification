# get_query_from_API.py collect json query from petfinder API

import json
import requests
from tqdm import tqdm

# original curl command
# : curl -d "grant_type=client_credentials&client_id={CLIENT-ID}&client_secret={CLIENT-SECRET}" https://api.petfinder.com/v2/oauth2/token
# : curl -H "Authorization: Bearer {YOUR_ACCESS_TOKEN}" GET https://api.petfinder.com/v2/{CATEGORY}/{ACTION}?{parameter_1}={value_1}&{parameter_2}={value_2}

def get_imageURL(api_key_path = './api_account.json', file_path = './test.json', page_number = 500):

    with open('./api_account.json', 'r', encoding='UTF-8') as f:
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




    params['page'] = 4183
    response = requests.get('https://api.petfinder.com/v2/animals', headers=headers, params=params)
    json_object = json.loads(response.text)

           
        

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_object, f, ensure_ascii=False, indent="\t")


if __name__ == '__main__':
    get_imageURL()