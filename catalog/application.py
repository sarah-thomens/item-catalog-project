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
def restaurantMenuJSON(book_id):
	book = session.query(Book).filter(Book.id == book_id).one()
	return jsonify(book = book.serialize)

#--------------------------------------------------------------------------------
# Website Route Functions
#--------------------------------------------------------------------------------
#--Show Recently Added Books-----------------------------------------------------
@app.route('/')
@app.route('/recent/')
def showRecentBooks():
	recentBooks = session.query(Book).order_by(desc(Book.id)).limit(10).all()
	return render_template('listBooks.html', book_type = 'Recently Added', books = recentBooks)

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
	if request.method == 'POST':
		urlSafe = request.form['title'].replace(' ', '-').lower()
		urlSafe = re.sub(r'[^a-zA-Z0-9-]', '', urlSafe)
		newBook = Book(title = request.form['title'], urlSafeTitle = urlSafe, author = request.form['author'], description = request.form['description'], genre = request.form['genre'], user_id = 1)
		session.add(newBook)
		session.commit()
		return redirect(url_for('showRecentBooks'))
	else:
		return render_template('addEdit.html')

#--Edit Book Information---------------------------------------------------------
@app.route('/book/<int:book_id>/<book_title>/edit', methods=['GET','POST'])
def editBook(book_title, book_id):
	editedBook = session.query(Book).filter(Book.id == book_id).one()
	print(editedBook.title)
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
	if request.method == 'POST':
		session.delete(bookToDelete)
		session.commit()
		return redirect(url_for('showRecentBooks'))
	else:
		return render_template('delete.html', book = bookToDelete)

#--------------------------------------------------------------------------------
# Website Login and Login Route Functions
#--------------------------------------------------------------------------------
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
	newUser = User(name = login_session['name'], email = login_session['email'],
		picture = login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter(User.email == login_session['email']).one()
	return user.id


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
