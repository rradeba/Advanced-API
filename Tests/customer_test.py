import unittest
from unittest import mock
from app import create_app  
from flask import jsonify

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    @mock.patch('Controllers.customerController.save_customer')
    def test_create_customer(self, mock_save_customer):
        mock_save_customer.return_value = jsonify({"message": "Customer saved"}), 201
        response = self.client.post('/customer', json={
            'customer_id': '001',
            'customer_name': 'John Smith',
            'customer_email': 'john_smith@email.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Customer saved', response.get_data(as_text=True))

    def test_create_customer_invalid_input(self):
        response = self.client.post('/customer', json={
            'customer_name': 'John Smith'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    @mock.patch('Controllers.customerController.get_customer')
    def test_get_customer_not_found(self, mock_get_customer):
        mock_get_customer.return_value = jsonify({"message": "Customer not found"}), 404
        response = self.client.get('/customer/999')
        self.assertIn('Customer not found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
