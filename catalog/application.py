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

#--Connect to Database and create database session--------------------------------
engine = create_engine('sqlite:///booksCatalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#--Show Recently Added Books------------------------------------------------------
@app.route('/')
@app.route('/recent/')
def showRecentBooks():
	recentBooks = session.query(Book).order_by(desc(Book.id)).limit(10).all()
	return render_template('listBooks.html', book_type = 'Recently Added', books = recentBooks)

#--Show Specific Genre of Books---------------------------------------------------
@app.route('/genre/<book_genre>')
def showGenreBooks(book_genre):
	editGenre = book_genre.replace( '-', ' ' ).title()
	genreBooks = session.query(Book).filter(Book.genre == book_genre)
	return render_template('listBooks.html', book_type = editGenre, books = genreBooks)

#--Show Book Information----------------------------------------------------------
@app.route('/book/<int:book_id>/<book_title>')
def showBookInfo(book_title, book_id):
	book = session.query(Book).filter(Book.id == book_id).one()
	return render_template('bookInfo.html', book = book)

#--Add Book Information-----------------------------------------------------------
@app.route('/book/add', methods=['GET','POST'])
def addBook():
	if request.method == 'POST':
		urlSafe = request.form['title'].replace(' ', '-').lower()
		urlSafe = re.sub(r'[^a-zA-Z0-9-]', '', urlSafe)
		newBook = Book(title = request.form['title'], urlSafeTitle = urlSafe, author = request.form['author'], description = request.form['description'], genre = request.form['genre'], user_id = 1)
		session.add(newBook)
		session.commit()
		flash('New Book %s Successfully Created' % (newBook.title))
		return redirect(url_for('showRecentBooks'))
	else:
		return render_template('addEdit.html')

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
