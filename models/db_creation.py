from sqlalchemy import create_engine
from .base_model import Base
from .users_model import User
from .products_model import Product
from .categories_model import Category
from .favourites_model import Favourite


def create_db():
    engine = create_engine("sqlite:///models/project_5_db")
    Base.metadata.create_all(engine)
