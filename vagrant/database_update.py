from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# get rows with name equal to Veggie Burger in MenuItem table
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger').all()
for veggieBurger in veggieBurgers:
    print(veggieBurger.id)
    print(veggieBurger.price)

# get first row with id equal to 8 in MenuItem table
urbanVeggieBurger = session.query(MenuItem).filter_by(id = 8).one()
print(urbanVeggieBurger)
# update menu item's price
urbanVeggieBurger.price = '$2.99'
# update row in db
session.add(urbanVeggieBurger)
session.commit()
