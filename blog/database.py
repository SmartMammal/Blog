"""
Database.py:
* Basic boiler plate for working with db using SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from blog import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"]) # Create the engine to talk to the db at the db URI specified in config
Base = declarative_base() #create a declarative base
Session = sessionmaker(bind=engine) 
session = Session() #start a new session