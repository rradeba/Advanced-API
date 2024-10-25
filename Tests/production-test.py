import unittest
from unittest.mock import patch
from app import app

class TestProduction(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('production.save_production') 
    def test_create_production(self, mock_save_production):
        mock_save_production.return_value = True
        response = self.app.post('/production', json={
            'production_id': '001',
            'product_id': '002',
            'production_quantity': '32',
            'production_date': '10/11/12'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Success', response.get_data(as_text=True))

        mock_save_production.assert_called_once_with({
            'production_id': '001',
            'product_id': '002',
            'production_quantity': '32',
            'production_date': '10/11/12'
        })

    @patch('production.save_production')  
    def test_production_missing_fields(self, mock_save_production):
        response = self.app.post('/production', json={
            'production_id': '001'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Input', response.get_data(as_text=True))

        mock_save_production.assert_not_called()  

    @patch('production.get_production')  
    def test_get_production_not_found(self, mock_get_production):
        mock_get_production.return_value = None 
        response = self.app.get('/production/001')  
        self.assertEqual(response.status_code, 404)  
        self.assertIn('Production not found', response.get_data(as_text=True))

        mock_get_production.assert_called_once_with('001') 

if __name__ == '__main__':
    unittest.main()

