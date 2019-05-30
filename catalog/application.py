from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book, User
from flask import session as login_session
import random, string

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
@app.route('/<book_title>')
def showBookInfo(book_title):
	book_title = book_title.replace('-', ' ').title()
	book = session.query(Book).filter(Book.title == book_title).one()
	return render_template('bookInfo.html', book = book)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
