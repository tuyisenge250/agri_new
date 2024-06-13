from sqlalchemy import Column, String, ForeignKey
from models.base_models import Base_model

class Resource(Base_model):
    __tablename__ = 'resource'
    crops = Column(String(60), nullable=False)
    content = Column(String(255), nullable=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
