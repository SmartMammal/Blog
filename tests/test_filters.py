# This is called a unittest... testing how a particular system works

import os
import unittest
import datetime

# Configure your app to use the testing configuration
# Note that class TestingConfig(object) function in config that this uses
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

import blog
from blog.filters import *

#Run the tests using PYTHONPATH=. python tests/test_filters.py
# PYTHONPATH environemtn variable set so the tests can import the blog module correctly, even through it is in a different location to the test files

class FilterTests(unittest.TestCase):

  """
  Creates a datetime.date object and runs it through the dateformat function 
  and makes sure that the resulting string is correct.
  """
  def testDateFormat(self):
    # Tonight we're gonna party...
    date = datetime.date(1999, 12, 31)
    formatted = dateformat(date, "%y/%m/%d")
    self.assertEqual(formatted, "99/12/31")

  """
  Passes None into the function and makes sure that you get a None object back in return
  """  
  def testDateFormatNone(self):

    formatted = dateformat(None, "%y/%m/%d")
    self.assertEqual(formatted, None)

    
if __name__ == "__main__":
    unittest.main()