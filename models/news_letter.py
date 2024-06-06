import models
from sqlalchemy import Column, String, LargeBinary, ForeignKey
from models.base_models import Base_model
from sqlalchemy.orm import relationship

class News(Base_model):
    __tablename__ = 'news'
    title = Column(String(128), nullable=False)
    content = Column(String(255), nullable=False)
    status = Column(String(128), nullable=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)