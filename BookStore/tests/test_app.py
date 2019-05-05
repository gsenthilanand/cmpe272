# Ref: https://pybit.es/simple-flask-api.html
# https://github.com/pybites/blog_code/blob/master/flaskapi/test_app.py 

from copy import deepcopy
#import unittest
import json

# Ref: https://stackoverflow.com/questions/34913348/flask-object-has-no-attribute-post-error-for-login-unit-test
# Ref: https://pythonhosted.org/Flask-Testing/
from flask_testing import TestCase 
from flask import Flask

from .context import bookstore # needed by pytest & therefore travis
#import bookstore.webapi 
from bookstore import webapi
from bookstore.webapi.app import app

BASE_BOOK_URL = 'http://127.0.0.1:5000/api/v1.0/books'
BAD_BOOK_URL = '{}/5'.format(BASE_BOOK_URL)
GOOD_BOOK_URL = '{}/3'.format(BASE_BOOK_URL)

# Ref: https://realpython.com/python-web-applications-with-flask-part-iii/ 
class TestFlaskApi(TestCase):
    # If you don’t define create_app a NotImplementedError will be raised.
    def create_app(self):
        app.config.from_object(self)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.backup_items = deepcopy(app.books)  # no references!
        self.app = app.test_client()
        self.app.testing = True

    #@app.route('/api/v1.0/books', methods=['GET'])
    def test_get_books(self):
        response = self.client.get(BASE_BOOK_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['books']), 2)

    # #@app.route('/api/v1.0/books/<int:BOOK_id>', methods=['GET'])
    # def test_get_one_BOOK(self):
    #     response = self.client.get("%s%s" % (BASE_BOOK_URL, '/2'))
    #     data = json.loads(response.get_data())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(data['BOOK']), 1)

    def tearDown(self):
        # reset app.items to initial state
        app.books = self.backup_items

