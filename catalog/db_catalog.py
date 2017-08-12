from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context
import os, sys

Base = declarative_base()

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    items = relationship('Item', backref="category")
    @property
    def serialize(self):
        "Return data"
        return {
                'name': self.name,
                'id': self.id
               }

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250))
    time = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    @property
    def serialize(self):
        return {
                'name': self.name,
                'id': self.id,
                'description': self.description,
                'category_id': self.category_id
               }

# user account
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    email = Column(String)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password(self,password):
        return custom_app_context.verify(password, self.password_hash)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

