from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)

    favourite_products = relationship("Favourite", cascade="all, delete-orphan", backref="user")


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    brands = Column(String(100))
    categories = Column(String(150))
    code = Column(Integer)
    nutriscore_grade = Column(String(1))
    product_name_fr = Column(String(200))
    stores = Column(String(100))

    @hybrid_property
    def url(self):
        return "https://fr.openfoodfacts.org/produit/" + str(self.code)


class Favourite(Base):
    __tablename__ = "favourite"

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    replaced_product = Column(Integer)

    def __init__(self, product):
        self.product = product

    product = relationship("Product", lazy="joined")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
