from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import declarative_base
from models.base_models import Base_model,Base
import models
from models.blogs import Blog
from models.news_letter import News
from models.product import Product
from models.resource import Resource
from models.user import User
from models.weather import Weather

classes = {
    "blogs": Blog,
    "news": News,
    "product": Product,
    "resource": Resource,
    "user": User,
    "weather": Weather
}

class DBstorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format('tuyisenge', 'tuyisenge2003', 'localhost', 'agrinew')
        )
        self.reload() 

    def all(self, cls=None):
        new_dict = {}
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            if cls not in classes.values():
                return new_dict

            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                new_dict[key] = obj
        else:
            for clss in classes.values():
                objs = self.__session.query(clss).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sess_factory)

    def close(self):
        self.__session.remove()

    def get(self, cls, id):
        if isinstance(cls, str):
            cls = classes.get(cls)
        if cls not in classes.values():
            return None

        return self.__session.query(cls).get(id)

    def count(self, cls=None):
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            if cls not in classes.values():
                return 0
            return self.__session.query(cls).count()
        else:
            total = 0
            for clss in classes.values():
                total += self.__session.query(clss).count()
            return total
