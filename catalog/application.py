from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book, User
from flask import session as login_session
import random, string
import re

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

#--Connect to Database and create database session-------------------------------
engine = create_engine('sqlite:///booksCatalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#--------------------------------------------------------------------------------
# Website JSON Endpoints
#--------------------------------------------------------------------------------
#--Book Catalog JSON Endpoint----------------------------------------------------
@app.route('/catalog/JSON')
def booksJSON():
	books = session.query(Book).all()
	return jsonify(books = [b.serialize for b in books])

#--Specific Book JSON Endpoint---------------------------------------------------
@app.route('/book/<int:book_id>/JSON')
def specificBookJSON(book_id):
	book = session.query(Book).filter(Book.id == book_id).one()
	return jsonify(book = book.serialize)

#--Specific User JSON Endpoint---------------------------------------------------
@app.route('/user/<int:user_id>/JSON')
def userJSON(user_id):
	user = session.query(User).filter(User.id == user_id).one()
	return jsonify(user = user.serialize)

#--------------------------------------------------------------------------------
# Website Route Functions
#--------------------------------------------------------------------------------
#--Show Recently Added Books-----------------------------------------------------
@app.route('/')
@app.route('/recent/')
def showRecentBooks():
	recentBooks = session.query(Book).order_by(desc(Book.id)).limit(10).all()
	return render_template('listBooks.html', book_type = 'Recently Added', books = recentBooks)

#--Show All Books----------------------------------------------------------------
@app.route('/books/all')
def showAllBooks():
	books = session.query(Book).order_by(Book.genre.asc(), Book.title.asc()).all()
	return render_template('myAllBooks.html', book_type = "All", books = books)

#--Show My Books----------------------------------------------------------------
@app.route('/books/my')
def showMyBooks():
	if 'username' not in login_session:
		return redirect('/login')
	books = session.query(Book).filter(Book.user_id == login_session['user_id']).order_by(Book.genre.asc(), Book.title.asc())
	return render_template('myAllBooks.html', book_type = "My", books = books)

#--Show Specific Genre of Books--------------------------------------------------
@app.route('/genre/<book_genre>')
def showGenreBooks(book_genre):
	editGenre = book_genre.replace( '-', ' ' ).title()
	genreBooks = session.query(Book).filter(Book.genre == book_genre)
	return render_template('listBooks.html', book_type = editGenre, books = genreBooks)

#--Show Book Information---------------------------------------------------------
@app.route('/book/<int:book_id>/<book_title>')
def showBookInfo(book_title, book_id):
	book = session.query(Book).filter(Book.id == book_id).one()
	return render_template('bookInfo.html', book = book)

#--Add Book Information----------------------------------------------------------
@app.route('/book/add', methods=['GET','POST'])
def addBook():
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		urlSafe = request.form['title'].replace(' ', '-').lower()
		urlSafe = re.sub(r'[^a-zA-Z0-9-]', '', urlSafe)
		newBook = Book(title = request.form['title'], urlSafeTitle = urlSafe, author = request.form['author'], description = request.form['description'], genre = request.form['genre'], user_id = login_session['user_id'])
		session.add(newBook)
		session.commit()
		return redirect(url_for('showRecentBooks'))
	else:
		return render_template('addEdit.html')

#--Edit Book Information---------------------------------------------------------
@app.route('/book/<int:book_id>/<book_title>/edit', methods=['GET','POST'])
def editBook(book_title, book_id):
	editedBook = session.query(Book).filter(Book.id == book_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editedBook.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this book. Please create your own book in order to edit.');}</script><body onload='myFunction()'>"
	if request.method == 'POST':
		if request.form['title']:
			editedBook.title = request.form['title']
			urlSafe = request.form['title'].replace(' ', '-').lower()
			urlSafe = re.sub(r'[^a-zA-Z0-9-]', '', urlSafe)
			editedBook.urlSafeTitle = urlSafe
		if request.form['author']:
			editedBook.author = request.form['author']
		if request.form['description']:
			editedBook.description = request.form['description']
		if request.form['genre']:
			editedBook.genre = request.form['genre']
		session.add(editedBook)
		session.commit()
		return redirect(url_for('showBookInfo', book_title = editedBook.title, book_id = editedBook.id))
	else:
		return render_template('addEdit.html', book = editedBook)

#--Delete Book Information-------------------------------------------------------
@app.route('/book/<int:book_id>/<book_title>/delete', methods=['GET','POST'])
def deleteBook(book_title, book_id):
	bookToDelete = session.query(Book).filter(Book.id == book_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if bookToDelete.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to delete this book. Please create your own book in order to delete.');}</script><body onload='myFunction()'>"
	if request.method == 'POST':
		session.delete(bookToDelete)
		session.commit()
		return redirect(url_for('showRecentBooks'))
	else:
		return render_template('delete.html', book = bookToDelete)

#--------------------------------------------------------------------------------
# Website Login and Login Route Functions
#--------------------------------------------------------------------------------
#--Login Route-------------------------------------------------------------------
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)

@app.route('/disconnect')
def disconnect():
	if 'provider' in login_session:
		if login_session['provider'] == 'google':
			gdisconnect()
			del login_session['gplus_id']
			del login_session['access_token']
		if login_session['provider'] == 'facebook':
			fbdisconnect()
			del login_session['facebook_id']

		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['user_id']
		del login_session['provider']
		return redirect(url_for('showRecentBooks'))
	else:
		return redirect(url_for('showRecentBooks'))

#--Gconnect route to connect using Google+ Oauth---------------------------------
@app.route('/gconnect', methods=['POST'])
def gconnect():
	#--Validate state token------------------------------------------------------
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	#--Obtain authorization code-------------------------------------------------
	code = request.data

	try:
		#--Upgrade the authorization code into a credentials object--------------
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	#--Check that the access token is valid.-------------------------------------
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	#--If there was an error in the access token info, abort.--------------------
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response
	#--Verify that the access token is used for the intended user.---------------
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	#--Verify that the access token is valid for this app.-----------------------
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response
	# Check to see if user is already logged in
	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['provider'] = 'google'
	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt':'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	# See if user exists, if it doesn't make a new one
	user_id = getUserID(login_session['email'])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']

	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("You are now logged in as %s" % login_session['username'])
	print "done!"
	return output


# DISCONNECT - Revoke a current user's token and reset their login_session.
@app.route("/gdisconnect")
def gdisconnect():
	# Only disconnect a connected user.
	access_token = login_session.get('access_token')
	if access_token is None:
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Execute HTTP GET request to revoke current token.
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':
		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		# For whatever reason, the given token was invalid.
		response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
		response.headers['Content-Type'] = 'application/json'
		return response

#--Get User Id using Email Helper Function---------------------------------------
def getUserID(email):
	try:
		user = session.query(User).filter(User.email == email).one()
		return user.id
	except:
		return None

#--Get User Information using User ID Helper Function----------------------------
def getUserInfo(user_id):
	user = session.query(User).filter(User.id == user_id).one()
	return user

#--Create User using the Login Session Helper Function---------------------------
def createUser(login_session):
	print(login_session)
	newUser = User(name = login_session['username'], email = login_session['email'],
		picture = login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter(User.email == login_session['email']).one()
	return user.id


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
