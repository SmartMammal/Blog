"""
Models.py:
* Creates the an SQLAlchemy model used to store and retrieve blog posts
"""

import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import ForeignKey #for one-to-many relationship between user and post model
from sqlalchemy.orm import relationship #for one-to-many relationship between user and post model

from database import Base, engine

class Post(Base): #create a new class which inherits from the declarative base object
    __tablename__ = "posts" #Give the model a table name
    
    #add a series of columns
    id = Column(Integer, primary_key=True) #primary key id
    title = Column(String(1024)) #title of the post
    content = Column(Text) #post content
    datetime = Column(DateTime, default=datetime.datetime.now) #date & time post created
    author_id = Column(Integer, ForeignKey('users.id')) #for one-to-many relationship between user and post model

#Create a User Model
#inherits from the declarative base
#inherits from Flask-Login's UserMixin class -- has default authentication methods
from flask.ext.login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True) #an integer id
    name = Column(String(128)) #a name
    email = Column(String(128), unique=True) #a unique email address which you will use to identify the user
    password = Column(String(128)) #and a password
    posts = relationship("Post", backref="author") #for one-to-many relationship between user and post model
    
Base.metadata.create_all(engine) #onstruct the table in the database
"""
#! 2. To create a migration script. Run python manage.py db migrate from the command line
#! 3. Run the migration to actually apply the changes to the database by saying python manage.py db upgrade
"""