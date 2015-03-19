# These are acceptance tests... basically allows you to test from a user's perspective
# Run the tests in command line using... PYTHONPATH=. python test_views_acceptance
# Selenium runs through the actions in the background

# CONSIDERATIONS:
# a. Unit tests: run quickly but only give you information about isolated sections of code
# b. Integration tests: run a little less quickly, and give you information about how different elements are working together
# c. Acceptance tests (this one): run slower still, but give you information that your whole system is working correctly

import os
import unittest
import multiprocessing #starts the Flask test server running; browser will visit actual site so you need a server up to run app
import time
from urlparse import urlparse

from werkzeug.security import generate_password_hash

from splinter import Browser
"""
a) Splinter is a userfriendly Python layer on top of the Selenium browser automation tool. Selenium allows us to automatically control an instance of a browser, ie visiting sites, clicking on links and adding content as if you were a real user.
b) In command line, run:
 i) pip install splinter; followed by
 ii) pip freeze > requirements.txt
c) You also need to install a browser which Selenium can control. Because the tests will be running on the Nitrous.IO server with no screen attached you cannot use a traditional browser like Chrome, or Firefox. Fortunately there is a project called Phantom JS, which is a headless version of the WebKit engine which power Safari. To install this on Nitrous, run parts install phantomjs.
"""
# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs") # Rather than test_client, we create instance of splinter.Browser, we use PhantomJS driver

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()
        
        #starts the Flask test server running; this gets the server up to run app
        self.process = multiprocessing.Process(target=app.run) #Target tells it which function to run -- app.run method in this case
        self.process.start() #You start the process using this
        time.sleep(1) # You need to wait a little for the server to start; this pauses for 1 second


    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate() #this kills the server
        session.close()
        Base.metadata.drop_all(engine)
        self.browser.quit() #this make the browser exit
        
    def testLoginCorrect(self): #tests that the login system works when correct
        self.browser.visit("http://0.0.0.0:8080/login") #Visit the login page
        self.browser.fill("email", "alice@example.com") #Fill the username section (looks for <input> element with matching name)
        self.browser.fill("password", "test") #Fill the password section of the form
        button = self.browser.find_by_css("button[type=submit]") #Find the submit button; it uses css selector rules to find an item (in this case a <button> element)
        button.click() #Use the click method to submit the form
        self.assertEqual(self.browser.url, "http://0.0.0.0:8080/") #Check to make sure that you have been relocated to the correct location (front page if logged successfully or back to login if incorrect)

    def testLoginIncorrect(self): #tests that the login system works when incorrect
        self.browser.visit("http://0.0.0.0:8080/login")
        self.browser.fill("email", "bob@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://0.0.0.0:8080/login")

if __name__ == "__main__":
    unittest.main()