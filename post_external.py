import requests
import json
from google.cloud import storage
def get_columnNames():
    url = "https://www.mirrormedia.mg/json/grouped.json"
    file = requests.get(url)
    data = json.loads(file.text)
    column_name = list(data['grouped'][0].keys())
    column_name.append('publishedDate')
    return column_name
def get_data(url):
    file = requests.get(url)
    data = json.loads(file.text)
    data = data['_items']
    return data
def get_post_results(data):
    column_names = get_columnNames()
    results = []
    for item in data:
        result = {}
        for columnName in column_names:
            if(columnName in item):
                result[columnName] = item[columnName]
            else:
                result[columnName] = ""
        results.append(result)
    return results
def get_external_results(data):
    column_names = get_columnNames()
    results = []
    for item in data:
        result = {}
        for columnName in column_names:
            if(columnName in item):
                result[columnName] = item[columnName]
            else:
                result[columnName] = ""
        result['slug'] = item['_id'] 
        result['heroImage'] = item['thumb'] 
        results.append(result)
    return results
def join_post_external(results1, result2):
    results = results1
    for i in result2:
        results.append(i)
    return results

def homepage_json() :
    column_names = get_columnNames()
    url_post_p1 = "https://api.mirrormedia.mg/posts?sort=-updateAt&where=%7B%22isAdvertised%22:false,%22state%22:%7B%22$ne%22:%22invisible%22%7D,%22categories%22:%7B%22$nin%22:%5B%22581c3a7792c2930d009de311%22,%225ea94861a66f9e0f00a0503f%22%5D%7D%7D&max_results=100&page=1"
    url_post_p2 = "https://api.mirrormedia.mg/posts?sort=-updateAt&where=%7B%22isAdvertised%22:false,%22state%22:%7B%22$ne%22:%22invisible%22%7D,%22categories%22:%7B%22$nin%22:%5B%22581c3a7792c2930d009de311%22,%225ea94861a66f9e0f00a0503f%22%5D%7D%7D&max_results=100&page=2"
    post_p1 = get_post_results(get_data(url_post_p1))
    post_p2 = get_post_results(get_data(url_post_p2))

    url_external_p1 = "https://api.mirrormedia.mg/externals?max_results=100&sort=-publishedDate&page=1"
    url_external_p2 = "https://api.mirrormedia.mg/externals?max_results=100&sort=-publishedDate&page=2"
    extetnal_p1 = get_external_results(get_data(url_external_p1))
    extetnal_p2 = get_external_results(get_data(url_external_p2))

    post_external = join_post_external(join_post_external(post_p1, post_p2), join_post_external(extetnal_p1, extetnal_p2))
    post_external = sorted(post_external, key=lambda k:k['publishedDate'])
    json_file = {'_items': post_external}
    with open('post_external.json', 'w') as f:
        json.dump(json_file, f)
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

