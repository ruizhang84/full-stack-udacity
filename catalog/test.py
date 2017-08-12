from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db_catalog import Base, Category, Item
import os, sys

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def categoryShow():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc(Item.time)).limit(7).all()
    return render_template('welcome.html', categories=categories, items=items)

@app.route('/category/v1/<category_name>/items')
def categoryMenu(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).first()
    items = session.query(MenuItem).filter_by(category_id=category.id).all()
    return render_template('menu.html', categories=categories, category=category, items=items)

@app.route('/catagory/v1/<int:item_id>/')
def description(item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    return render_template('descript.html', item=item)

@app.route('/category/v1/<int:category_id>/new', methods=['GET', 'POST'])
def newMenuItem(category_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], category_id=category_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('itemMenu', category_id=category_id))
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template('newmenu.html', category=category, category_id=category_id)

# Task 2: Create route for editMenuItem function here

@app.route('/category/v1/<int:category_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(category_id, menu_id):
    if request.method == 'POST':
        item = session.query(Item).filter_by(id=menu_id).one()
        if request.form['name']:
            item.name = request.form['name']
        session.add(item)
        session.commit()
        return redirect(url_for('categoryMenu', category_id=category_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=category_id).one()
        return render_template('editmenu.html', restaurant=restaurant, category_id=category_id, menu_id=menu_id)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/v1/<int:category_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(category_id, menu_id):
    if request.method == 'POST':
        item = session.query(Item).filter_by(id=menu_id).one()
        session.delete(item)
        session.commit()
        return redirect(url_for('categoryMenu', category_id=category_id))
    else:
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('deletemenu.html', item=item, category_id=category_id, menu_id=menu_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)