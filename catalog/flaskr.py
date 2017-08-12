from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response
from flask import flash, jsonify
from flask_httpauth import HTTPBasicAuth
from flask import session as login_session
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db_catalog import Base, Category, Item, User
from form import SignupForm, SigninForm
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os, sys, random, string, requests, httplib2, json

auth = HTTPBasicAuth()
app = Flask(__name__)
#os.urandom(32)
app.secret_key = '\xd4\x9bV\xb3\xfe\xef\xa9l\xd7\x90\xb9\x82\xa99\xd1$ad"\x80\'\xca=*\xfe\'.\xba\xff\xa7\xb5Y'

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()

#########################################
#Json session
@app.route('/catalog.json')
def CategoryJSON():
    json_cat = []
    categories = session.query(Category).all()
    for cat in categories:
        temp = cat.serialize
        items = session.query(Item).filter_by(category_id=cat.id).all()
        temp['items'] = [i.serialize for i in items]
        json_cat.append(temp)
    return jsonify(Category=json_cat)

#########################################
#basic view
@app.route('/')
def categoryShow():
    categories = session.query(Category).all()
    latest_items = session.query(Item).order_by(desc(Item.time)).limit(7).all()
    items = []
    for item in latest_items:
        category = session.query(Category).filter_by(id=item.category_id).first()
        items.append([category.name, item.name])
    return render_template('welcome.html', categories=categories, items=items, login_session=login_session)

@app.route('/catalog/<category_name>/items')
def categoryMenu(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).first()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('menu.html', categories=categories, category=category, items=items, login_session=login_session)

@app.route('/catalog/<category_name>/<item_name>')
def description(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).first()
    item = session.query(Item).filter_by(name=item_name, category_id=category.id).one()
    return render_template('descript.html', category=category, item=item, login_session=login_session)

@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

#########################################
#login session
@app.route('/catalog/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        newuser = User(username=form.username.data, email=form.email.data)
        newuser.hash_password(form.password.data)
        session.add(newuser)
        session.commit()
        login_session['email'] = form.email.data
        return redirect(url_for('categoryShow'))
    return render_template('signup.html', form=form)

@app.route('/catalog/signin', methods=['POST', 'GET'])
def signin():
    if 'email' in login_session:
        return redirect(url_for('categoryShow'))

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state

    form = SigninForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = session.query(User).filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return redirect(url_for('signin'))
        login_session['email'] = user.email
        return redirect(url_for('categoryShow'))
    return render_template('signin.html', form=form, state=state)

@app.route('/catalog/signout')
def signout():
    login_session.pop('email', None)
    login_session.pop('state', None)
    if 'access_token' in login_session:
        access_token = login_session['access_token']
        userinfo_url = "https://accounts.google.com/o/oauth2/revoke"
        params = {'token': access_token}
        requests.get(userinfo_url, params=params)
        login_session.pop('access_token', None)
    return redirect(url_for('categoryShow'))

@app.route('/catalog/gconnect/<state>', methods=['POST'])
def gconnect(state):
    # Validate state token
    if state != login_session['state']:
        respose = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    #print (code, file=sys.stderr)

    # Upgrade the authorization code into a credentials object
    try:
        flow = flow_from_clientsecrets('client_secrets.json',
                               scope='')
        flow.redirect_uri = 'postmessage'
        credentials = flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #http_auth = httplib2.Http()
    #http_auth = credentials.authorize(http_auth)
    login_session['access_token'] = credentials.access_token

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['email'] = data['email']
    resp = make_response("Accepted", 200)
    return resp

#########################################
#Add/Edit session
@app.route('/catalog/new', methods=['POST', 'GET'])
def newItem():
    #if 'email' in login_session:
    #    return redirect(url_for('categoryShow'))
    categories = session.query(Category).all()

    if request.method == 'POST':
        #check if name has been used.
        oldItem = session.query(Item).filter_by(category_id=request.form['category'], name=request.form['name']).first()
        if oldItem is not None:
            return render_template('new.html', categories=categories)
        newItem = Item(name=request.form['name'], description=request.form['descript'], \
                       time=datetime.utcnow() , category_id=request.form['category'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('categoryShow'))
    return render_template('new.html', categories=categories, login_session=login_session)

@app.route('/catalog/<item_name>/edit', methods=['POST', 'GET'])
def editItem(item_name):
    #if 'email' in login_session:
    #    return redirect(url_for('categoryShow'))

    categories = session.query(Category).all()
    item = session.query(Item).filter_by(name=item_name).first()
    if request.method == 'POST':
        if request.form['name'] is not None:
            item.name = request.form['name']
        if request.form['descript'] is not None:
            item.description = request.form['descript']
        if request.form['category'] is not None:
            item.category_id = request.form['category']
        session.add(item)
        session.commit()
        return redirect(url_for('categoryShow'))
    return render_template('edit.html', categories=categories, item=item, login_session=login_session)

@app.route('/catalog/<item_name>/delete', methods=['POST', 'GET'])
def deleteItem(item_name):
    #if 'email' in login_session:
    #    return redirect(url_for('categoryShow'))
    item = session.query(Item).filter_by(name=item_name).first()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('categoryShow'))
    return render_template('delete.html', login_session=login_session)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)







