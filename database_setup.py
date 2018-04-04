
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# creates instance of declarative base
Base = declarative_base()

# restaurant class
class Restaurant(Base):
    # table
    __tablename__ = 'restaurant'
    # mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

# menu item class
class MenuItem(Base):
    # table
    __tablename__ = 'menu_item'
    # mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

# creates database and adds tables and columns
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
