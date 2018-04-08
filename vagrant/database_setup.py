
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

    @property
    def serialize(self):
        # returns object data in easily serializable format
        return {
            'name': self.name,
            'id': self.id
        }

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

    @property
    def serialize(self):
        # returns object data in easily serializable format
        return {
            'name': self.name,
            'id': self.id,
            'course': self.course,
            'description': self.description,
            'price': self.price,
            'restaurant_id': self.restaurant_id
        }

# creates database and adds tables and columns
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
