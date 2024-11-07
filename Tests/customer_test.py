import unittest
from unittest import mock
from app import create_app
from flask import jsonify
from extensions import db
from Controllers.customerController import save_customer, get_customer

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    @mock.patch('Controllers.customerController.save_customer')
    def test_create_customer(self, mock_save_customer):
        # Mock the save_customer function response
        mock_save_customer.return_value = jsonify({"message": "Customer saved"}), 201

        response = self.client.post('/customer/', json={
            'customer_id': 1,
            'customer_name': 'John Smith',
            'customer_email': 'john_smith@email.com',
            'customer_phone': '1234567890'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"message": "Customer saved"})
        self.assertTrue(mock_save_customer.called)

    def test_create_customer_invalid_input(self):
        response = self.client.post('/customer/', json={
            'customer_name': 'John Smith'  # Missing required fields
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    @mock.patch('Controllers.customerController.get_customer')
    def test_get_customer_not_found(self, mock_get_customer):
        mock_get_customer.return_value = jsonify({"message": "Customer not found"}), 404
        response = self.client.get('/customer/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Customer not found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
