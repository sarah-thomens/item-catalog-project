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
book = Book(user_id = 1, title = "Uprooted", author = "Naomi Novik", description = "Agnieszka's whole life turns upside down when the Dragon chooses her as tribute.", image = "static/uprooted.jpg", genre = "fantasy")
session.add(book)
session.commit()

book = Book(user_id = 1, title = "There's No Place Like Here", author = "Cecelia Ahern", description = "Sandy Shortt has been obsessed with finding lost things since she was little. Now, she's the lost thing.", image = "static/TNPLH.jpg", genre = "magical-realism")
session.add(book)
session.commit()

book = Book(user_id = 1, title = "The Scarlet Letter", author = "Nathaniel Hawthorne", description = "Hester Prynne has been sentenced to public shame, being forced to wear the scarlet letter A across her chest for the rest of her life.", image = "static/ScarletLetter.jpg", genre = "classic")
session.add(book)
session.commit()

print "Books Added!"
