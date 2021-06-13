# from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)

    favourite_products = relationship("Favourite", cascade="all, delete-orphan", backref="user")

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    brands = Column(String(100))
    categories = Column(String(150))
    code = Column(Integer)
    nutriscore_grade = Column(String(1))
    product_name_fr = Column(String(200))
    stores = Column(String(100))


class Favourite(Base):
    __tablename__ = "favourite"

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    replaced_product = Column(Integer)

    def __init__(self, product):
        self.product = product

    product = relationship("Product", lazy="joined")
