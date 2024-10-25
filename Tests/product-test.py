import unittest
from unittest.mock import patch
from app import app

class TestProduct(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('product.save_product')  
    def test_create_product(self, mock_save_product):
        mock_save_product.return_value = True
        response = self.app.post('/product', json={
            'product_id': '001',
            'product_name': 'Car',
            'product_price': '100.10'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Success', response.get_data(as_text=True))

        mock_save_product.assert_called_once_with({
            'product_id': '001',
            'product_name': 'Car',
            'product_price': '100.10'
        })

    @patch('product.save_product')  
    def test_product_missing_fields(self, mock_save_product):
        response = self.app.post('/product', json={
            'product_id': '001'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Input', response.get_data(as_text=True))

        mock_save_product.assert_not_called() 

    @patch('product.get_product') 
    def test_get_product_not_found(self, mock_get_product):
        mock_get_product.return_value = None 
        response = self.app.get('/product/001')  
        self.assertEqual(response.status_code, 404)  
        self.assertIn('Product not found', response.get_data(as_text=True))

        mock_get_product.assert_called_once_with('001')  

if __name__ == '__main__':
    unittest.main()
