import models
from sqlalchemy import Column, String, LargeBinary, ForeignKey, Integer
from models.base_models import Base_model
from sqlalchemy.orm import relationship

class Product(Base_model):
    __tablename__ = 'products'
    name = Column(String(60), nullable=False)
    price = Column(String(50), nullable=False)
    type = Column(String(30), nullable=True)
    image = Column(String(255), nullable=False)
    discription = Column(String(255), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)