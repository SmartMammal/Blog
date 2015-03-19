# This is called an integration tests... testing how subsystems interact together correctly.

import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True

    def testAddPost(self):
        self.simulate_login() #Act as a logged in user

        response = self.client.post("/post/add", data={
            "title": "Test Post",
            "content": "Test content"
        }) #send a POST request using client.post, using data parameter to provide the form data for an example post
        
        #Next check that the response from the app looks correct
        self.assertEqual(response.status_code, 302) #Check user redirected to the "/" route by checking the status code
        self.assertEqual(urlparse(response.location).path, "/") #Check redirection by checking location header of the response
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1) #check post has been added to the database correctly

        post = posts[0]
        self.assertEqual(post.title, "Test Post") #Title set to the right value
        self.assertEqual(post.content, "<p>Test content</p>\n") #content set to the right value
        self.assertEqual(post.author, self.user) #autho set to the right value
        
if __name__ == "__main__":
    unittest.main()