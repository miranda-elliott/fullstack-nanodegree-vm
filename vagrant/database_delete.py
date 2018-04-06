from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# get first row with name equal to Spinach Ice Cream in MenuItem table
spinachIceCream = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
# delete row
session.delete(spinachIceCream)
session.commit()
