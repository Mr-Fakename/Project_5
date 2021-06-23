import requests


class API:
    def __init__(self):
        self.raw_data = None
        self.cleaned_data = []

    def get_data(self):
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
        self.raw_data = r.json()

    def cleaner(self):
        """ Takes json data that was extracted from the OpenFoodFacts API with the 'get_data()' function
            Dict comprehension checks if some values are missing. If it is the case, the associated key
            is deleted.
            The function then loops over all products and stores those containing all the keys we want to use,
            ensuring we only work with complete data.
        """

        self.raw_data = [{key: value for key, value in product.items() if value} for product in self.raw_data["products"]]

        tags = ['brands', 'categories', 'code', 'nutriscore_grade', 'product_name_fr', 'stores']

        for product in self.raw_data:
            if all(key in product for key in tags):
                self.cleaned_data.append(product)
