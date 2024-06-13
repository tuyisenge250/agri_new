import models
from sqlalchemy import Column, String, ForeignKey
from models.base_models import Base_model
from sqlalchemy.orm import relationship

class News(Base_model):
    __tablename__ = 'news'
    title = Column(String(128), nullable=False)
    content = Column(String(255), nullable=False)
    status = Column(String(128), nullable=False)
    image = Column(String(255), nullable=False, default='images systems')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)