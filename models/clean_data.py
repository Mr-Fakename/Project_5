import json


def cleaner():
    """ Takes json data that was extracted from the OpenFoodFacts API with 'api_calls.py'
        Dict comprehension checks if some values are missing. If it is the case, the associated key
        is deleted.
        The function then loops over all products and stores those containing all the keys we want to use,
        ensuring we only work with complete data.
    """

    with open("API_data.json") as data:
        data = json.load(data)

    data = [{key: value for key, value in product.items() if value} for product in data["products"]]

    tags = ['brands', 'categories', 'code', 'nutriscore_grade', 'product_name_fr', 'stores', 'url']
    cleaned_data = []

    for product in data:
        if all(key in product for key in tags):
            cleaned_data.append(product)

    return cleaned_data


def make_readable(cleaned_data):
    """ Performs string formatting; proper capitalization, and makes lists from keys with several values.
        Individual values will be stored in database.

        A new json file is then created.
    """

    for product in cleaned_data:
        product["product_name_fr"] = product['product_name_fr'].title()
        product["nutriscore_grade"] = product["nutriscore_grade"].upper()

        product["brands"] = product["brands"].title().split(",")
        product["categories"] = product["categories"].title().split(",")
        product["stores"] = product["stores"].title().split(",")

    with open('cleaned_data.json', 'w') as f:
        json.dump(cleaned_data, f, indent=4)

