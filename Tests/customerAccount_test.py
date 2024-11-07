import unittest
from unittest import mock
from app import create_app  
from flask import jsonify
from extensions import db 
from Controllers.customerAccountController import save_customer_account, get_customer_account, update_customer_account, delete_customer_account

class TestCustomerAccount(unittest.TestCase):
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

    @mock.patch('Controllers.customerAccountController.save_customer_account')  
    def test_create_customer_account(self, mock_save_customer_account):
        mock_save_customer_account.return_value = jsonify({"message": "Customer account saved"}), 201
        response = self.client.post('/customer/account', json={
            'customer_username': 'john_smith',
            'customer_password': 'securepassword'
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"message": "Customer account saved"})
        self.assertTrue(mock_save_customer_account.called)

    def test_create_customer_account_invalid_input(self):
        response = self.client.post('/customer/account', json={
            'customer_username': 'john_smith'  # Missing password field
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    @mock.patch('Controllers.customerAccountController.get_customer_account')  
    def test_get_customer_account_not_found(self, mock_get_customer_account):
        mock_get_customer_account.return_value = jsonify({"message": "Customer account not found"}), 404
        response = self.client.get('/customer/account/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"message": "Customer account not found"})

    @mock.patch('Controllers.customerAccountController.update_customer_account')  
    def test_update_customer_account(self, mock_update_customer_account):
        mock_update_customer_account.return_value = jsonify({"message": "Customer account updated"}), 200
        response = self.client.put('/customer/account/1', json={
            'customer_password': 'newsecurepassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Customer account updated"})

    @mock.patch('Controllers.customerAccountController.delete_customer_account')  
    def test_delete_customer_account(self, mock_delete_customer_account):
        mock_delete_customer_account.return_value = jsonify({"message": "Customer account deleted"}), 200
        response = self.client.delete('/customer/account/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Customer account deleted"})

if __name__ == '__main__':
    unittest.main()
