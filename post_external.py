import requests
import json
from google.cloud import storage

column_names =["slug","title", "style", "sections", "categories", "heroImage", "brief", "publishedDate"]
def get_results(url, api_endpoint, results):
    file = requests.get(url)
    data = json.loads(file.text)
    data = data['_items']
    for item in data:
        result = {}
        for columnName in column_names:
            if(columnName in item):
                result[columnName] = item[columnName]
            else:
                result[columnName] = ""
        if api_endpoint == "externals":
            result['slug'] = item['_id'] 
            result['heroImage'] = item['thumb'] 
        results.append(result)
    return results   
def homepage_json():
    results = []
    api_endpoints= ["posts", "externals"]
    mm_url = "https://api.mirrormedia.mg/"
    post_parameter = "?sort=-updateAt&where=%7B%22isAdvertised%22:false,%22state%22:%7B%22$ne%22:%22invisible%22%7D,%22categories%22:%7B%22$nin%22:%5B%22581c3a7792c2930d009de311%22,%225ea94861a66f9e0f00a0503f%22%5D%7D%7D&max_results=100&page="
    external_parameter = "?max_results=100&sort=-publishedDate&page="
    results = []
    for api_endpoint in api_endpoints:
        if api_endpoint == "posts":
            parameter = post_parameter
        else:
            parameter = external_parameter

        for i in range(1, 3):
            url = mm_url + api_endpoint +parameter + str(i)
            get_results(url, api_endpoint, results)

    results = sorted(results, key=lambda k:k['publishedDate'])
    post_external = {'_items': results}
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


homepage_json()
upload_blob('statics.mirrormedia.mg', 'post_external.json', 'statics.mirrormedia.mg/json/json/post_external.json')

