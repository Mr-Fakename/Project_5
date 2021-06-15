from models.api_calls import API
from models.clean_data import make_readable
from models.SA_models import Product, User, Category, Favourite

from sqlalchemy.orm import Session
from sqlalchemy import create_engine


class Database:
    def __init__(self):
        self.engine = create_engine("sqlite:///models/project_5")
        self.session = Session(self.engine)

        self.user = None

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

    def create_user(self, username):
        new_user = User(username=username.capitalize())
        self.session.add(new_user)
        self.session.commit()
        print(f"User: {new_user.username}, created!")

    def find_user(self):
        while self.user is None:
            print("Please type your name to select your user profile:")
            users = self.session.query(User).filter(User.username.ilike(f"%{input()}%"))
            if len([user for user in users]) == 1:
                self.user = [user for user in users][0]
                print(f"Hello, {self.user.username}!")
            elif len([user for user in users]) == 0:
                print("No user was found; either because they don't exist, or you mistyped")
                continue
            else:
                print("Your input returned several values, please choose below:")
                print([user.username for user in users])
                continue

    def display_favourites(self):
        return self.user.favourite_products

    def display_products_in_category(self, category):
        products_in_category = self.session.query(Product).filter(Product.categories.ilike(f"%{category}%"))
        return [product for product in products_in_category]

    def add_favourite(self, product):
        self.user.favourite_products.append(Favourite(product))

    def delete_favourite(self, favourite):
        self.display_favourites().remove(favourite)

    def display_categories(self):
        categories = self.session.query(Category).all()
        return [category.name for category in categories]

    def display_replacement(self, product):
        print(product.product_name_fr, product.nutriscore_grade)
        query = self.session.query(Product).filter(Product.nutriscore_grade < product.nutriscore_grade)
        return [result for result in query]

# myAPI = API()
# myAPI.get_data()
# myAPI.cleaner()
# cleaned_data = make_readable(myAPI.cleaned_data)

db = Database()
db.find_user()
products = db.display_products_in_category("sauces")
product = products[0]
