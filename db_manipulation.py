from models.api_calls import API
from models.clean_data import make_readable
from models.SA_models import Product, User, Category, Favourite

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


class Database:
    def __init__(self):
        self.engine = create_engine("sqlite:///models/project_5")
        self.session = Session(self.engine)

    def fill_db(self, cleaned_data):

        categories = []

        for product in cleaned_data:
            new_product = Product(
                brands=product["brands"],
                categories=product["categories"],
                code=product["code"],
                nutriscore_grade=product["nutriscore_grade"],
                product_name_fr=product["product_name_fr"],
                stores=product["stores"]
            )
            self.session.add(new_product)
            categories.append(new_product.categories.split(", ")[:2])

        self.session.commit()

        categories = [category for sublist in categories for category in sublist]
        categories = sorted(categories, key=categories.count, reverse=True)

        def duplicate_removal(iterable):
            seen = set()
            seen_add = seen.add
            return [x for x in iterable if not (x in seen or seen_add(x))][:14]

        categories = duplicate_removal(categories)

        for category in categories:
            new_category = Category(
                name=category
            )
            self.session.add(new_category)

        self.session.commit()


    # def query_db(self, nutriscore):
    #     products = self.session.query(Product).filter_by(nutriscore_grade=nutriscore)
    #     return [product for product in products]

    def create_user(self, username):
        new_user = User(username=username)
        self.session.add(new_user)
        self.session.commit()
        print("User created!")

    def find_user(self, username):
        # users = self.session.query(User).filter_by(username=username)
        users = self.session.query(User).filter(User.username.ilike(f"%{username}%"))
        return [user for user in users]

    def display_favourites(self, category):
        # categories = self.session.query(Category).all()
        products_in_category = self.session.query(Product).filter(Product.categories.ilike(f"%{category}%"))
        return [product for product in products_in_category]

    def display_product(self):
        pass

    def add_favourite(self):
        pass

    def delete_favourite(self):
        pass

    def display_categories(self):
        categories = self.session.query(Category).all()
        return categories

    def display_replacement(self):
        pass


# myAPI = API()
# myAPI.get_data()
# myAPI.cleaner()
# cleaned_data = make_readable(myAPI.cleaned_data)

db = Database()
categories = db.display_categories()
for category in categories:
    print(category.name)
# db.fill_db(cleaned_data)
# product = db.query_db("E")[0]
# db.create_user("John")
# users = db.find_user(input())
# products = db.display_categories()
query = db.display_favourites(input())
