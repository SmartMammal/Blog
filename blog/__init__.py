import os
from flask import Flask #import the Flask object

app = Flask(__name__) #create your app in the usual way

# Load the configuration into the __init__.py file
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig") #Try to get environment variable to configuration object; if unavailable will go to default. This is easy way to switch over to different configuration: testing, development and production
app.config.from_object(config_path) # Use use this method to configure the app using the object specified

#These imports come after the app; they make use of the app object
import views #import your various views
import filters #import your various filters

from . import login #import your login routines


