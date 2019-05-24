#--SQLAlchemy imports to make the database work properly------------------------------------------------------
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

#--The User Class Table---------------------------------------------------------------------------------------
class User(Base):
	__tablename__ = 'user'

	#--Table Column Fields------------------------------------------------------------------------------------
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	email = Column(String(250), nullable = False)
	picture = Column(String(250))

	#--Return the object data in an easily serializable format------------------------------------------------
	@property
	def serialize(self):
		return
		{
			'id'		: self.id,
			'name'		: self.name,
			'email'		: self.email,
			'picture'	: self.picture
		}


#--The Book Class Table---------------------------------------------------------------------------------------
class Book(Base):
	__tablename__ = 'book'

	#--Table Column Fields------------------------------------------------------------------------------------
	id = Column(Integer, primary_key = True)
	title = Column(String(250), nullable = False)
	author = Column(String(250))
	description = Column(String(500))
	image = Column(String(250))
	genre = Column(String(250))
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	#--Return the object data in an easily serializable format------------------------------------------------
	@property
	def serialize(self):
		return
		{
			'id': self.id,
			'title': self.title,
			'author': self.author,
			'description': self.description,
			'image': self.image,
			'genre': self.genre
		}


#--Engine to create the books catalog-------------------------------------------------------------------------
engine = create_engine('sqlite:///booksCatalog.db')

Base.metadata.create_all(engine)
