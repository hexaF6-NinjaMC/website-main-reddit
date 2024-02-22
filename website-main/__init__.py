
from flask import Flask
from flask_sqlalchemy import SQLAlchemy #this will be used to store our database
from flask_login import LoginManager
#from flask_alembic import Alembic       #this will be used to migrate database when changes are made, flask_migrate might be better but both are tricky
from os import path

#https://hackersandslackers.com/flask-application-factory/


#create instances of plugin objects
db = SQLAlchemy()

DB_NAME = "database.db"


def create_app():
    
    #create a flask application
    app = Flask(__name__)

    #configure the flask application, this can be done through a config file as well
    app.config["SECRET_KEY"] = "fpwbsl"                     #key used to sign session cookies to protect against data tampering
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}" 
    
    #initialize(bind) plugin objects to our flask application
    db.init_app(app)                   

    #import blueprints 
    from .views import views            # the '.' before views tells the interpreter to search the current location of which views.py is a member
    from .auth import auth
    from .models import User, Flashcard      #only two classes in models but "from . import models" didn't work. 

    #register blueprints
    app.register_blueprint(views, url_prefix = '/')     #https://flask.palletsprojects.com/en/2.2.x/blueprints/
    app.register_blueprint(auth, url_prefix = '/')      #registering the Blueprint objects create in views.py and auth.py

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        #print(User.query.get(id).is_authenticated) combination of flask_sqlalchemy.sqlalchemy.database.query and flask_login.UserMixin
        return User.query.get(id)

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
            with app.app_context():             #with is exception handling , note some tutorials say to use this  when registering blueprints(above)
                db.create_all()                 #https://hackersandslackers.com/flask-application-factory/
                print("Created Database!")