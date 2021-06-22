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
        """ Creates a User object in the database and returns that object
            Username is passed as an input()
        """
        new_user = User(username=username.capitalize())
        return new_user

    def get_user(self):
        """ ORM method to retrieve User objects in the database, equivalent to:
        SELECT user.id AS user_id, user.username AS user_username
        FROM user
        WHERE lower(user.username) LIKE lower(?)
        """
        users = self.session.query(User).filter(User.username.ilike(f"%{input()}%"))
        return users

    def get_favourites(self):
        """ Returns a collection of objects associated with a User object in the database
        In SQLAlchemy, a many-to-many relationship can be represented in different ways;
        in this case it is an association object : https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
        """
        return self.user.favourite_products

    def get_products_in_category(self, category):
        """ Returns a list of Product objects that match a SELECT statement, based on the category
        they belong to (e.g. snacks, dairy...)
        ORM equivalent to:
        SELECT * FROM product WHERE lower(product.categories) LIKE lower(?)
        """
        products_in_category = self.session.query(Product).filter(Product.categories.ilike(f"%{category}%"))
        return [product for product in products_in_category]

    def add_favourite(self, replacement, replaced):
        """ Function that exists to simplify adding a Favourite object to a User
        Takes "replacement" and "replaced" parameters to refer to Product objects in the database and retrieve their
        associated data
        """
        return self.user.favourite_products.append(Favourite(replacement, replaced))

    def delete_favourite(self, favourite):
        """ Simple function that takes a Product object present in a Favourite relationship,
        and deletes it from the collection, then saves the changes in the DB
        """
        self.user.favourite_products.remove(favourite)
        self.session.commit()

    def get_categories(self):
        """ Return the name of all Category objects saved in the database """
        categories = self.session.query(Category).all()
        return [category.name for category in categories]

    def get_replacement(self, product, category):
        """ Returns a list of Product objects that belong to the category passed as the "category" parameter,
        and have a better nutriscore grade than the Product object passed as parameter
        (e.g. "A" < "C" == True)
        ORM equivalent to:
        SELECT *
        FROM product
        WHERE product.nutriscore_grade < ? AND lower(product.categories) LIKE lower(?)
        """
        query = self.session.query(Product).filter(Product.nutriscore_grade < product.nutriscore_grade,
                                                   Product.categories.ilike(f"%{category}%")
                                                   )
        return [result for result in query]
