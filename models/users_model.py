from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base_model import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)

    favourite_products = relationship("Favourite",
                                      cascade="all, delete-orphan",
                                      backref="user")
