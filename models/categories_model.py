from sqlalchemy import Column, Integer, String
from .base_model import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
