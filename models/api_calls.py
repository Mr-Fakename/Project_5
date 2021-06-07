import requests
import json


url = "https://fr.openfoodfacts.org/cgi/search.pl?"
headers = {"User-Agent": "PurBeurre/OpenClassRooms - Python/Windows - Version 1.0"}
payload = {"search_simple": 1,
           "action": "process",
           "tagtype_0": "countries",
           "tag_contains_0": "contains",
           "tag_0": "france",
           "sort_by": "unique_scans_n",
           "page_size": 1000,
           "json": 1,
           "fields": "brands,url,stores,nutriscore_grade,"
                     "categories,product_name_fr,code"
           }

r = requests.get(url, params=payload, headers=headers)

r_json = r.json()

with open('API_data.json', 'w') as f:
    json.dump(r_json, f, indent=4)
