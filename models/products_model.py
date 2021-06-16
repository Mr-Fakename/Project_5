from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from .base_model import Base


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
