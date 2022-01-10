import requests
import json
import math
from google.cloud import storage
from config import column_names, api_endpoints_url_dict, api_base_url, max_results
def get_results(url, api_endpoint):
    results = []
    file = requests.get(url)
    data = json.loads(file.text)
    data = data['_items']
    for item in data:
        result = {}
        for column_name in column_names:
            if(column_name in item):
                result[column_name] = item[column_name]
            else:
                result[column_name] = ""
        if api_endpoint == "externals":
            result['slug'] = item['_id']
            result['heroImage'] = item['thumb']
        results.append(result)
    return results
def homepage_json():
    post_external = []
    page = math.ceil(max_results/100)
    for api_endpoint in api_endpoints_url_dict.keys():
        for i in range(1, page):
            url = api_base_url + api_endpoint + \
                api_endpoints_url_dict[api_endpoint] + str(i)
            post_external += get_results(url, api_endpoint)
    post_external = sorted(post_external, key=lambda k: k['publishedDate'])
    post_external = {'_items': post_external}
    with open('post_external.json', 'w') as f:
        json.dump(post_external, f)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

if __name__ == "__main__":
    homepage_json()
    upload_blob('statics.mirrormedia.mg', 'post_external.json',
                'statics.mirrormedia.mg/json/json/post_external.json')


