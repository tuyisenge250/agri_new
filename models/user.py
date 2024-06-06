import models
from sqlalchemy import Column, String, LargeBinary
from models.base_models import Base_model
from sqlalchemy.orm import relationship

class User(Base_model):
    __tablename__ = 'users'
    email = Column(String(128), nullable=False, unique=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    password = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    image = Column(String(255), default="")
    blogs = relationship('Blog', back_populates='user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
