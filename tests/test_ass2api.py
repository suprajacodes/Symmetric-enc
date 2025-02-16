import unittest
from flask import Flask
from flask.testing import FlaskClient
from ass2api import app

class Ass2ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_encrypt(self):
        response = self.client.post('/encrypt', json={'text': 'Hello world'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('cipher', data)
        self.assertIn('iv', data)

if __name__ == '__main__':
    unittest.main()
