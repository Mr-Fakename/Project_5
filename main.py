from models.db_manipulation import Database
from models.api_caller import API
from models.api_data_cleaner import make_readable
from models.db_creation import *


if __name__ == '__main__':
    # off_api = API()
    # off_api.get_data()
    # off_api.cleaner()
    # data = make_readable(off_api.cleaned_data)
    # db.fill_db(data)

    db = Database()
    # db.create_user(input())
    db.get_user()
    # print(db.get_categories())
    products = db.get_products_in_category("snacks")
    product = products[0]
    print(product.product_name_fr, product.nutriscore_grade)
    replacement = db.get_replacement(product, "snacks")[0]
    print(replacement.product_name_fr, replacement.nutriscore_grade)
    db.add_favourite(replacement, product)