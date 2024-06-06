import models
from sqlalchemy import Column, String, LargeBinary
from models.base_models import Base_model
from sqlalchemy.orm import relationship

class Weather(Base_model):
    __tablename__ = 'weather'
    Location = Column(String(128), nullable=False)
    high_temperature = Column(String(30), nullable=False)
    low_temperature = Column(String(30), nullable=False)
    wind = Column(String(30), nullable=True)
    change = Column(String(30), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)