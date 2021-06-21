from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from .users_model import User
from .products_model import Product
from .categories_model import Category
from .favourites_model import Favourite


class Database:
    """
    Class that connects to the database and contains all the methods to interact with it, via
    the SQLAlchemy ORM
    """

    def __init__(self):
        self.engine = create_engine("sqlite:///models/project_5_db")
        self.session = Session(self.engine)

        self.user = None

    def fill_db(self, cleaned_data):
        """
        This function is the link between API data and the database
        The cleaned data in entry is JSON and each key/value keeps the same name in the DB

        Categories are obtained by keeping track of how many times they appear for each product,
        sorting them by count and keeping the 15 most represented
        """
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
            categories.append(new_product.categories.split(", ")[:1])

        self.session.commit()

        categories = [category for sublist in categories for category in sublist]
        categories = sorted(categories, key=categories.count, reverse=True)

        # The 3 following lines delete duplicate categories and keep them in order
        seen = set()
        seen_add = seen.add
        categories = [x for x in categories if not (x in seen or seen_add(x))][:15]

        for category in categories:
            new_category = Category(
                name=category
            )
            self.session.add(new_category)

        self.session.commit()

    @staticmethod
    def add_user(username):
        new_user = User(username=username.capitalize())
        return new_user

    def get_user(self):
        users = self.session.query(User).filter(User.username.ilike(f"%{input()}%"))
        return users

    def get_favourites(self):
        return self.user.favourite_products

    def get_products_in_category(self, category):
        products_in_category = self.session.query(Product).filter(Product.categories.ilike(f"%{category}%"))
        return [product for product in products_in_category]

    def add_favourite(self, replacement, replaced):
        return self.user.favourite_products.append(Favourite(replacement, replaced))

    def delete_favourite(self, favourite):
        self.user.favourite_products.remove(favourite)
        self.session.commit()

    def get_categories(self):
        categories = self.session.query(Category).all()
        return [category.name for category in categories]

    def get_replacement(self, product, category):
        query = self.session.query(Product).filter(Product.nutriscore_grade < product.nutriscore_grade,
                                                   Product.categories.ilike(f"%{category}%")
                                                   )
        return [result for result in query]
