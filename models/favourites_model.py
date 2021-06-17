from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import Base


class Favourite(Base):
    __tablename__ = "favourite"

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    replaced_product = Column(Integer)

    def __init__(self, product, replaced_product):
        self.product = product
        self.replaced_product = replaced_product.id

    product = relationship("Product", lazy="joined")
