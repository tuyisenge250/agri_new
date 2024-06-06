from sqlalchemy import Column, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from models.base_models import Base_model

class Blog(Base_model):
    __tablename__ = 'blogs'
    
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    blog = Column(String(255), nullable=False)
    image = Column(String(255), nullable=True)
    
    user = relationship('User', back_populates='blogs')