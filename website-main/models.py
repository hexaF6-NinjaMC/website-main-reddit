from . import db            #from this package(website) import db(defined in __init__.py)
from flask_login import UserMixin           #class that provdes basic implimentation that flask_login expects(e.g. 'is_authenticated')
                                                #https://flask-login.readthedocs.io/en/latest/
from sqlalchemy.sql import func             #func will be used to get timestamps



#https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
#when a new user or note for user is created it will be added to the database session with the the values
#defined by "column"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
                                                                  #one to many, relationship will allow for many Decks per User. 
    decks = db.relationship("Deck",  back_populates = "user")       # backref is a reverse link, This would be used to get the User of a Note
                                                                    #note that the backref value can be whatever you want, it adds a property
                                                                    #to an instantiated Note that points to User
    
    flashcards = db.relationship("Flashcard",  back_populates = "user") # "user" is referencing the User class, no sure why it has to be lc

    
class Deck(db.Model):
    id = db.Column(db.Integer)
    title = db.Column(db.String(100), primary_key = True) #unique = True wasn't working so going to use this to make sure no duplicate deck names
    
    #many to one relationship with deck as child and user as parent
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    user = db.relationship("User", back_populates = "decks") 

    #flashcard children to Deck parent.  
    flashcards = db.relationship("Flashcard", back_populates = "deck")         
    




class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    data = db.Column(db.Text)
    data2 = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone = True), default = func.now())            #get current timestamp
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  #user.id references the User, sql is inconsistent with capitalization, see "Note" above
    
    #relate to deck
    deck_title = db.Column(db.Integer, db.ForeignKey('deck.title')) #tied this to title instead of ID as if it is a new deck we don't know the ID before commit to DB
    deck = db.relationship("Deck", back_populates = "flashcards")

    #relate to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    user = db.relationship("User", back_populates = "flashcards")
    




#if I wanted to have videos, reminders, just set up another class
#class Reminder(db.model)