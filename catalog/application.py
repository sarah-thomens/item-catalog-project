from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
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

#--Connect to Database and create database session------------------------------------------------------------
engine = create_engine('sqlite:///booksCatalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#--Show Recently Added Books----------------------------------------------------------------------------------
@app.route('/')
@app.route('/recent/')
def showRecentBooks():
	recentBooks = session.query(Book)
	return render_template('recentlyAdded.html', recentBooks = recentBooks)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
