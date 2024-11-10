import unittest
from services.cart.cart_service import app
import json

class TestCart(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_add_to_cart(self):
        response = self.app.post('/api/cart/add/1', 
                               json={'quantity': 1})
        self.assertEqual(response.status_code, 200)
    
    def test_view_cart(self):
        response = self.app.get('/api/cart')
        self.assertEqual(response.status_code, 200)
