import unittest
from unittest import mock
from app import create_app  
from extensions import db
from Controllers.orderController import save_order, get_order  

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
        mock_save_order.return_value = True 
        
        response = self.client.post('/order', json={
            'order_id': 1,
            'customer_id': 2,
            'product_id': 3,
            'quantity': 10,
            'total_price': 100.10
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('Success', response.get_data(as_text=True))

        
        mock_save_order.assert_called_once_with({
           'order_id': 1,
            'customer_id': 2,
            'product_id': 3,
            'quantity': 10,
            'total_price': 100.10
        })

    @mock.patch('Controllers.orderController.save_order')  
    def test_order_missing_fields(self, mock_save_order):
        response = self.client.post('/order', json={
            'order_id': 1 
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Input', response.get_data(as_text=True))

        
        mock_save_order.assert_not_called() 

    @mock.patch('Controllers.orderController.get_order')  
    def test_get_order_not_found(self, mock_get_order):
        mock_get_order.return_value = None 
        
        response = self.client.get('/order/1')  
        
        self.assertEqual(response.status_code, 404)  
        self.assertIn('Order not found', response.get_data(as_text=True))

        
        mock_get_order.assert_called_once_with('1')

if __name__ == '__main__':
    unittest.main()
