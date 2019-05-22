from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Book, User

engine = create_engine('sqlite:///booksCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#--Create a Dummy User----------------------------------------------------------------------------------------
dummyUser = User(name="Hermione Granger", email="h.granger@gmail.com",
						 picture='static/Hermione.webp')
session.add(dummyUser)
session.commit()

##--Creating Starter books for the book catalog database------------------------------------------------------
book1 = Book(user_id = 1, title = "Uprooted", author = "Naomi Novik", description = "Agnieszka's whole life turns upside down when the Dragon chooses her as tribute.", image = "static/uprooted.jpg", genre = "Fantasy")
session.add(book1)
session.commit()

print "Books Added!"
