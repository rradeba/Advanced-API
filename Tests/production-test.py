import unittest
from unittest import mock
from app import create_app  
from flask import jsonify
from extensions import db 
from Controllers.productionController import save_production, get_production 


class TestProduction(unittest.TestCase):
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

    @mock.patch('Controllers.productionController.save_production')  
    def test_create_production(self, mock_save_production):
        
        response = self.client.post('/production/', json={
            'production_id': 1,
            'production_quantity': 2
        })
        
        print(mock_save_production)
        print(response.get_json())
        print("Response JSON:", response.get_json())
        print("Mock was called:", mock_save_production.called)
        print("Mock call args:", mock_save_production.call_args)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('Production saved', response.get_data(as_text=True))

    def test_create_production_invalid_input(self):
        response = self.client.post('/production/', json={
            'production_quantity': 3 
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    @mock.patch('Controllers.productionController.get_production')  
    def test_get_production_not_found(self, mock_get_production):
        mock_get_production.return_value = jsonify({"message": "Production not found"}), 404
        response = self.client.get('/production/999')
        self.assertIn('Production not found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
