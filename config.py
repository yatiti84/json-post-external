
column_names = ["slug", "title", "style", "sections",
                "categories", "heroImage", "brief", "publishedDate","partner"]
api_endpoints_url_dict = {"posts": "?sort=-updateAt&where=%7B%22isAdvertised%22:false,%22state%22:%7B%22$ne%22:%22invisible%22%7D,%22categories%22:%7B%22$nin%22:%5B%22581c3a7792c2930d009de311%22,%225ea94861a66f9e0f00a0503f%22%5D%7D%7D&max_results=100&page=",
                                  "externals": "?max_results=100&sort=-publishedDate&page="}
api_base_url = "https://api.mirrormedia.mg/"
max_results = 200
