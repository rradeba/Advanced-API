import unittest
from unittest import mock
from app import create_app  
from flask import jsonify
from extensions import db 

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
        mock_save_product.return_value = jsonify({"message": "Product saved"}), 201
        response = self.client.post('/product/', json={
            'product_id': 1,
            'product_name': 'Widget',
            'product_price': 3.27
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"message": "Product saved"})
        self.assertTrue(mock_save_product.called)

    def test_create_product_invalid_input(self):
        response = self.client.post('/product/', json={
            'product_price': 2.27  # Missing product_name, which is required
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    @mock.patch('Controllers.productController.get_product')  
    def test_get_product_not_found(self, mock_get_product):
        mock_get_product.return_value = jsonify({"message": "Product not found"}), 404
        response = self.client.get('/product/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"message": "Product not found"})

if __name__ == '__main__':
    unittest.main()
