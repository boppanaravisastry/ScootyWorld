import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, backref

from sqlalchemy import create_engine

Model = declarative_base()


# class to store user data
class User(Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    profile_img = Column(String(250))


class Scooter_category(Model):
    __tablename__ = 'scooter_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    user_id = Column(String(500), ForeignKey('users.id'))
    user = relationship(User, backref="category")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id
        }


# class for scooty data
class Scooter(Model):
    __tablename__ = "scooters"

    id = Column(Integer, primary_key=True)
    model = Column(String(250), nullable=False)
    price = Column(String(250), nullable=False)
    image = Column(String(500), nullable=False)
    mileage = Column(String(250), nullable=False)
    fuel_capacity = Column(String(250), nullable=False)
    description = Column(String(1000), nullable=False)
    scooter_category_id = Column(Integer, ForeignKey('scooter_category.id'))
    scooter_category = relationship(Scooter_category, backref=backref(
        'scooters', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # return book data in serializable format
        return {
            'id': self.id,
            'model': self.model,
            'price': self.price,
            'mileage': self.mileage,
            'fuel_capacity': self.fuel_capacity,
            'image': self.image,
            'description': self.description
        }
engine = create_engine('sqlite:///ScooterWorld.db')
Model.metadata.create_all(engine)
print("tables are ready")
