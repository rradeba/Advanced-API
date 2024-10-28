import unittest
from unittest import mock
from app import create_app  
from flask import jsonify
from extensions import db 



class TestOrder(unittest.TestCase):
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

    @mock.patch('Controllers.orderController.save_order')  
    def test_create_order(self, mock_save_order):
        response = self.client.post('/order/', json={
            'order_id': 1,
            'order_quantity': 2,
            'total_price': 10.10
        })
        
        print(mock_save_order)
        print(response.get_json())
        print("Response JSON:", response.get_json())
        print("Mock was called:", mock_save_order.called)
        print("Mock call args:", mock_save_order.call_args)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('Order saved', response.get_data(as_text=True))

    def test_create_order_invalid_input(self):
        response = self.client.post('/order/', json={
            'order_quantity': 3  
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    @mock.patch('Controllers.orderController.get_order')  
    def test_get_order_not_found(self, mock_get_order):
        mock_get_order.return_value = jsonify({"message": "Order not found"}), 404
        response = self.client.get('/order/999')
        self.assertIn('Order not found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
