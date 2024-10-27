import unittest
from unittest import mock
from app import create_app  
from extensions import db
from Controllers.productController import save_product, get_product  

class TestProduct(unittest.TestCase):

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

    @mock.patch('Controllers.productController.save_product')  
    def test_create_product(self, mock_save_product):
        mock_save_product.return_value = True 
        
        response = self.client.post('/product', json={
            'product_id': 1,
            'product_name': 'Car',
            'product_price': 100.10
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('Success', response.get_data(as_text=True))

        
        mock_save_product.assert_called_once_with({
            'product_id': 1,
            'product_name': 'Car',
            'product_price': 100.10
        })

    @mock.patch('Controllers.productController.save_product')  
    def test_product_missing_fields(self, mock_save_product):
        response = self.client.post('/product', json={
            'product_id': 1  
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Input', response.get_data(as_text=True))

      
        mock_save_product.assert_not_called() 

    @mock.patch('Controllers.productController.get_product')  
    def test_get_product_not_found(self, mock_get_product):
        mock_get_product.return_value = None  
        
        response = self.client.get('/product/1')  
        
        self.assertEqual(response.status_code, 404)  
        self.assertIn('Product not found', response.get_data(as_text=True))

       
        mock_get_product.assert_called_once_with('1')

if __name__ == '__main__':
    unittest.main()
