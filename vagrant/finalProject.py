from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# create session and connect to db
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)
    # return 'This page will show all my restaurants'

@app.route('/restaurant/new', methods = ['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        restaurant = Restaurant(name = request.form['name'])
        session.add(restaurant)
        session.commit()
        flash('restaurant created!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('new_restaurant.html')
    # return 'This page will be for making a new restaurant'

@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash('restaurant edited!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('edit_restaurant.html', restaurant = restaurant)
    # return 'This page will be for editing restaurant %s' % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('restaurant deleted!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('delete_restaurant.html', restaurant = restaurant)
    # return 'This page will be for deleting restaurant %s' % restaurant_id

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', restaurant = restaurant, items = items)
    # return 'This page is the menu for restaurant %s' % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        item = MenuItem(name = request.form['name'], price = request.form['price'], description = request.form['description'], restaurant_id = restaurant_id)
        session.add(item)
        session.commit()
        flash('menu item created!')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant_id = restaurant_id)
    # return 'This page is for making a new menu item for restaurant %s' % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.price = request.form['price']
        item.description = request.form['description']
        session.add(item)
        session.commit()
        flash('menu item edited!')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('edit_menu_item.html', restaurant_id = restaurant_id, item = item)
    # return 'This page is for editing menu item %s' % menu_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('menu item deleted!')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('delete_menu_item.html', restaurant_id = restaurant_id, item = item)
    # return 'This page is for deleting menu item %s' % menu_id

# API endpoints
@app.route('/restaurants/JSON')
def getRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    json = []
    for restaurant in restaurants:
        json.append(restaurant.serialize)
    return jsonify(Restaurants = json)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def getRestaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    json = []
    for item in items:
        json.append(item.serialize)
    return jsonify(MenuItems = json)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def getRestaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = item.serialize)

if __name__ == '__main__':
    # reloads server every time code changes
    app.debug = True
    # allows to flash messages
    app.secret_key = 'super_secret_key'
    app.run(host = '0.0.0.0', port = 5000)
