from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify
from flask import session as session_login
from flask import make_response
from decorators import login_mandatory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from migrations import Model, Scooter, User, Scooter_category
import random
import string
import httplib2
import json
import requests

# oauth imports

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials

# configuring app

app = Flask(__name__)
app.secret_key = 'randomkey'

# Bind the engine to the metadata of the Model class so that the
# declaratives can be accessed through a DBSession instance

engine = create_engine('sqlite:///ScooterWorld.db',
                       connect_args={'check_same_thread': False}, echo=True)
Model.metadata.bind = engine

secret_file = json.loads(open('client_secret.json', 'r').read())
CLIENT_ID = secret_file['web']['client_id']

DBSession = sessionmaker(bind=engine)
session = DBSession()


# App Routes


def get_user_id():
    """it returns user id
    """
    user = session.query(User).filter_by(name=session_login["name"]).one()
    return user.id


def get_owner_id(cls, id):
    """it returns owner id of object
    """
    obj = session.query(cls).get(id)
    user = session.query(User).filter_by(name=session_login["name"]).one()
    return obj.user_id


@app.route('/')
@app.route('/scooters/')
def all_scooters():
    """it displays all scooters
    """
    scooters = session.query(Scooter).all()
    categories = session.query(Scooter_category).all()
    return render_template('index.html', scooters=scooters,
                           categories=categories, login_session=session_login)


@app.route('/scooters/category/<int:id>')
def category_scooters(id):
    """it displays all scooters which belongs to particular scooter category
    """
    categories = session.query(Scooter_category).all()
    print("id:", id)
    scooters = session.query(Scooter).filter_by(scooter_category_id=id).all()
    if len(scooters) == 0:
        flash("No scooters avialable from this category", "danger")
    return render_template('index.html', scooters=scooters,
                           categories=categories, login_session=session_login)


@app.route('/scooters/<int:scooter_id>', methods=["POST", "GET"])
def scooter_details(scooter_id):
    """
    this method displays details about the scooter which related to the id
    """
    categories = session.query(Scooter_category).all()
    scooter = session.query(Scooter).get(scooter_id)
    return render_template('scooter_details.html', scooter=scooter,
                           login_session=session_login, categories=categories)


def check_user():
    email = session_login['email']
    return session.query(User).filter_by(email=email).one_or_none()


@app.route('/scooters/<int:scooter_id>/delete', methods=["POST", "GET"])
def scooter_delete(scooter_id):
    """
    delete the scooter from database
    """
    user_id = get_user_id()
    owner_id = get_owner_id(Scooter, scooter_id)
    print(user_id, owner_id)
    if int(user_id) != int(owner_id):
        flash("You don't have permission to do this", "danger")
        return redirect("/")
    scooter = session.query(Scooter).get(scooter_id)
    session.delete(scooter)
    session.commit()
    flash("deleted successfully", "success")
    return redirect('/')


@app.route('/scooters/add', methods=["POST", "GET"])
@login_mandatory
def scooter_add():
    """
    it adds scooter into database
    """
    if request.method == 'POST':
        print('post')
        user = session.query(User).filter_by(name=session_login["name"]).one()
        print(user.id)
        scooter = Scooter(model=request.form["model"],
                          price=request.form["price"],
                          description=request.form["description"],
                          image=request.form["image"],
                          mileage=request.form["mileage"],
                          fuel_capacity=request.form["fuel_capacity"],
                          scooter_category_id=request.form["category"],
                          user_id=int(user.id)
                          )
        session.add(scooter)
        session.commit()
        flash('scooter saved successfully', 'success')
        return redirect('/')
    else:
        print('inside get')
        categories = session.query(Scooter_category).all()
        return render_template('scooter_add.html', categories=categories,
                               login_session=session_login)


@app.route('/scooters/<int:id>/edit', methods=["POST", "GET"])
@login_mandatory
def scooter_edit(id):
    """
    this method edits the details of th particular scooter
    """
    categories = session.query(Scooter_category).all()
    scooter = session.query(Scooter).get(id)
    user_id = get_user_id()
    owner_id = get_owner_id(Scooter, id)
    print(user_id, owner_id)
    if int(user_id) != int(owner_id):
        flash("You don't have permission to do this", "danger")
        return redirect("/")
    if request.method == 'POST':
        scooter.model = request.form["model"]
        scooter.price = request.form["price"]
        scooter.description = request.form["description"]
        scooter.image = request.form["image"]
        scooter.mileage = request.form["mileage"]
        scooter.fuel_capacity = request.form["fuel_capacity"]
        scooter.scooter_category_id = request.form["category"]
        session.commit()
        flash("scooter updated..", "success")
        return redirect('/')
    else:
        return render_template("scooter_edit.html", scooter=scooter,
                               categories=categories,
                               login_session=session_login)


@app.route('/scooters/categories/add', methods=["POST", "GET"])
@login_mandatory
def scooter_category_add():
    """
    this method adds the different categories of the scooters
    """
    if request.method == 'POST':
        name = request.form["name"]
        print(name)
        user = session.query(User).filter_by(name=session_login["name"]).one()
        scooter_category = Scooter_category(name=name,
                                            user_id=user.id)
        session.add(scooter_category)
        session.commit()
        flash('category saved successfully', 'success')
        return redirect('/')
    else:
        categories = session.query(Scooter_category).all()
        scooters = session.query(Scooter).all()
        return render_template('scooter_category_add.html',
                               categories=categories, scooters=scooters,
                               login_session=session_login)


@app.route('/scooters/categories/<int:id>/delete', methods=["POST", "GET"])
@login_mandatory
def scooter_category_delete(id):
    """
    this method deletes the particular category of the scooter
    """
    user_id = get_user_id()
    owner_id = get_owner_id(Scooter_category, id)
    print(user_id, owner_id)
    if int(user_id) != int(owner_id):
        flash("You don't have permission to do this", "danger")
        return redirect("/")
    scooter_category = session.query(Scooter_category).get(id)
    session.delete(scooter_category)
    session.commit()
    flash("category deleted", "success")
    return redirect('/')


@app.route('/scooters/categories/<int:id>/edit', methods=["POST", "GET"])
@login_mandatory
def scooter_category_edit(id):
    """
    this method update name of the category
    """
    categories = session.query(Scooter_category).all()
    scooter_category = session.query(Scooter_category).get(id)
    user_id = get_user_id()
    owner_id = get_owner_id(Scooter_category, id)
    print(user_id, owner_id)
    if int(user_id) != int(owner_id):
        flash("You don't have permission to do this", "danger")
        return redirect("/")
    if request.method == 'POST':
        print(user_id, owner_id)
        if int(user_id) == int(owner_id):
            scooter_category.name = request.form["name"]
            session.commit()
            return redirect('/')
        else:
            return "you are not a owner inside"
    else:
        return render_template("scooter_category_edit.html",
                               scooter_category=scooter_category,
                               login_session=session_login,
                               categories=categories)


@app.route('/login')
def login():
    """
    it displays the login page
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    session_login['state'] = state
    return render_template('signtemplate.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gConnect():
    """
    this method signup the user through gmail
    """
    if request.args.get('state') != session_login['state']:
        response.make_response(json.dumps('Invalid State paramenter'),
                               401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data
    try:

        # Upgrade the authorization code into a credentials object

        flow = flow_from_clientsecrets('client_secret.json',
                                       scope='', redirect_uri='postmessage')
        credentials = flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps("""Failed to upgrade the
        authorisation code"""), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    myurl = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token)
    header = httplib2.Http()
    result = json.loads(header.request(myurl, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
                            """Token's user ID does not
                            match given user ID."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            """Token's client ID
            does not match app's."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    stored_credentials = session_login.get('credentials')
    stored_gplus_id = session_login.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'),
                          200)
        response.headers['Content-Type'] = 'application/json'
        return response

    session_login['credentials'] = access_token
    session_login['id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # ADD PROVIDER TO LOGIN SESSION

    print("TYPE ", type(data), data.keys())
    try:
        session_login['name'] = data['name']
    except Exception:
        session_login['name'] = 'anonimus'
    session_login['img'] = data['picture']
    session_login['email'] = data['email']
    session_login['provider'] = 'google'
    if not check_user():
        createUser()
    return jsonify(name=session_login['name'],
                   email=session_login['email'],
                   img=session_login['img'])


def createUser():
    """
    this method will store the data of signin user
    """
    name = session_login['name']
    email = session_login['email']
    url = session_login['img']
    newUser = User(name=name, email=email, profile_img=url)
    session.add(newUser)
    session.commit()


@app.route('/logout', methods=['post'])
def logout():

    # Disconnect based on provider

    if session_login.get('provider') == 'google':
        return gdisconnect()
    else:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/gdisconnect')
def gdisconnect():
    access_token = session_login['credentials']

    # Only disconnect a connected user.

    if access_token is None:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % access_token
    header = httplib2.Http()
    result = header.request(url, 'GET')[0]

    if result['status'] == '200':

        # Reset the user's session.

        del session_login['credentials']
        del session_login['id']
        del session_login['name']
        del session_login['email']
        del session_login['img']
        session_login['provider'] = 'null'
        response = make_response(json.dumps({'state': 'loggedOut'}), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:

        # if given token is invalid, unable to revoke token

        response = make_response(json.dumps({'state': 'errorRevoke'}), 200)
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON Endpoints

@app.route('/scooters/JSON')
def scootersJSON():
    """
    it gives the scooters data in json format from database
    """
    scooters = session.query(Scooter).all()
    return jsonify(Scooters=[scooty.serialize for scooty in scooters])


@app.route('/scooters/category/<int:category_id>/JSON')
def scooterCategoryJSON(category_id):
    """
    it gives the scooter details which belongs to aparticular
    category in json format
    """
    scooters = session.query(Scooter).filter_by(
        scooter_category_id=category_id).all()
    return jsonify(scooters=[scooter.serialize for scooter in scooters])


@app.route('/categories/JSON')
def categoriesJSON():
    """
    it gives the scooter categories  in json format from database
    """
    categories = session.query(Scooter_category).all()
    return jsonify(Scooters=[category.serialize for category in categories])


@app.route('/scooters/category/<int:category_id>/<int:scooter_id>/JSON')
def arbitraryItemJSON(category_id,scooter_id):
    category = session.query(Scooter_category).filter_by(id=category_id).one()
    scooter = session.query(Scooter).filter_by(id=scooter_id,
        scooter_category=category).one()
    return jsonify(scooter=[scooter.serialize])

# to running our application
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
