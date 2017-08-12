from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db_catalog import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

category1 = Category(name='Snowboarding')
session.add(category1)
session.commit()

s = ("Close-fitting glasses with side shields,"
             "for protecting the eyes from glare, dust, water, etc.")

item1 = Item(name='Goggles', description=s, \
             time=datetime.utcnow() , category_id=category1.id)
session.add(item1)
session.commit()

s = ("A board resembling a short, broad ski"
             "used for sliding downhill on snow.")

item2 = Item(name='Snowboard', description=s,\
             time=datetime.utcnow() , category_id=category1.id)
session.add(item2)
session.commit()

category2 = Category(name='Soccer')
session.add(category2)
session.commit()