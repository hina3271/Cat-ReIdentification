import json
import os
import requests
import shutil
from tqdm import tqdm


'''Open json file and download cat image from url'''

def download_image(dir_path = './cat/', file_path = './meta_data.json'):
    with open(file_path, 'r', encoding='UTF-8') as f:
        json_object = json.load(f)

    pbar = tqdm(json_object['list_cat'])
    pbar.set_description("Downloading images")

    for cat in pbar:
        for i, url in enumerate(cat['photos']):
            filename = dir_path + str(cat['id']) + '_' + str(i) + '.jpg'
            try: 
                r = requests.get(url, stream=True)
                with open(filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    
            except requests.exceptions.Timeout as errd:
                print("Timeout Error : ", errd)

            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting : ", errc)
                
            except requests.exceptions.HTTPError as errb:
                print("Http Error : ", errb)

            # Any Error except upper exception
            except requests.exceptions.RequestException as erra:
                print("AnyException : ", erra)

if __name__ == '__main__':
    download_image()