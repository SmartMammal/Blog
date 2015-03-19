"""
Config.py:
* this class to contain the configuration variables which control the Flask app
* set the location of your database
* tell Flask to use its debug mode to help you track down any errors in your application
* Note SECRET_KEY setting:
a. used to cryptographically secure your application
b. don't put inside application configuration itself; instead, use os.environ.get to obtain the secret key from an environment variable
c. Enter this into terminal prompt: export BLOGFUL_SECRET_KEY="your_secret_key_here" ... this sets an environment variable called BLOGFUL_SECRET_KEY
"""

import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "") #Thinkful123
    
class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful-test" #Separate database URI for testing
    DEBUG = False # Turn off the debug setting
    SECRET_KEY = "TestThinkful123" #Use a different secret key
