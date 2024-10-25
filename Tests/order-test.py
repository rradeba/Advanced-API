import unittest
from unittest.mock import patch
from app import app

class TestOrder(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('order.save_order')
    def test_create_order(self, mock_save_order):
        mock_save_order.return_value = True
        response = self.app.post('/order', json={
            'order_id': '001',
            'customer_id': '002',
            'product_id': '003',
            'quantity': '10',
            'total_price': '100'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Success', response.get_data(as_text=True))

        mock_save_order.assert_called_once_with({
            'order_id': '001',
            'customer_id': '002',
            'product_id': '003',
            'quantity': '10',
            'total_price': '100'
        })

    @patch('order.save_order')
    def test_order_missing_fields(self, mock_save_order):
        response = self.app.post('/order', json={
            'order_id': '001'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Input', response.get_data(as_text=True))

        mock_save_order.assert_not_called() 

    @patch('order.get_order')
    def test_get_order_not_found(self, mock_get_order):
        mock_get_order.return_value = None 
        response = self.app.get('/order/001')  
        self.assertEqual(response.status_code, 404)  
        self.assertIn('Order not found', response.get_data(as_text=True))

        mock_get_order.assert_called_once_with('001')

if __name__ == '__main__':
    unittest.main()
