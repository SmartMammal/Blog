from flask.ext.login import LoginManager

from blog import app
from .database import session
from .models import User

login_manager = LoginManager() #create an instance of the LoginManager class from Flask-Login
login_manager.init_app(app) #initialize it

login_manager.login_view = "login_get" #name of the view which an unauthorized user will be redirected to when they try to access a protected resource
login_manager.login_message_category = "danger" #category used to classify any error messages from Flask-Login... used with Bootstrap's alerts system

@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))