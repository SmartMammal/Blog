"""
Manage.py:
* calls the app.run method to start your development server.
* contains a series of commands intended to help you out as you develop the application
* Use Flask-script to speed up rather than argparse
* Flask-Script is designed to allow you to easily specify tasks to help you manage your application
"""

import os
#Import the manager object
from flask.ext.script import Manager 

from blog import app

manager = Manager(app) #Create an instance of the manager object

@manager.command #add a command to the manager by decorating a function
def run(): #To call run function: python manage.py run
    port = int(os.environ.get('PORT', 8080)) #Get a report from environment; 8080 is default if unavailable
    app.run(host='0.0.0.0', port=port) #run development server

    
# NOTE: Why listen on a port specificed by an environment variable? It allows us to deploy on servers which don't have a fixed outgoing port or deploy on multiple servers each using a different outgoing port without having to change our code.

#Generate a series of posts to seed the application
from blog.models import Post
from blog.database import session

@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    for i in range(25):
        post = Post(
            title="Test Post #{}".format(i),
            content=content
        )
        session.add(post)
    session.commit()

#add a new user to test login system
from getpass import getpass
from werkzeug.security import generate_password_hash
from blog.models import User

#How it works...
#1. ask the user for their name, email address, and their password twice
#2. check to make sure that the user is not already stored in the database
#3. make sure that the passwords match
#4. create the user object and add it to the database

@manager.command
def adduser():
    name = raw_input("Name: ")
    email = raw_input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print "User with that email address already exists"
        return

    password = ""
    password_2 = ""
    while not (password and password_2) or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email,
                password=generate_password_hash(password)) # Uses has from werkzeug SHA1 hashing algorithm
    session.add(user)
    session.commit()
    
#Manage the Migration
#Uses Alembic on SQLAlchemy: http://alembic.readthedocs.org/en/latest/
#Flask-Migrate wrapper around alembic: http://flask-migrate.readthedocs.org/en/latest/
from flask.ext.migrate import Migrate, MigrateCommand
from blog.database import Base

class DB(object): #Holds the metadata object used by Alembic to work out what changes to do to database schema
    def __init__(self, metadata): 
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata)) #Create instance of Flask-Migrate passing in the app and instance of DB
manager.add_command('db', MigrateCommand)

#! 1. Remember, in command line do: python manage.py db init ... in order to initialize migrations

if __name__ == "__main__":
    manager.run() #run the manager