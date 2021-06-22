from sqlalchemy import create_engine
from .base_model import Base
from .users_model import User
from .products_model import Product
from .categories_model import Category
from .favourites_model import Favourite


def create_db():
    """ Establishes a connection between the chosen database and SQLAlchemy
    Drops the tables and recreates them, for an easy and efficient reset of the DB
    """
    engine = create_engine("sqlite:///models/project_5_db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
