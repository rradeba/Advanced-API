import unittest
from unittest.mock import patch
from app import app

class TestEmployee(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('employee.save_employee')  
    def test_create_employee_success(self, mock_save_employee):
        mock_save_employee.return_value = True
        response = self.app.post('/employee', json={
            'employee_id': '001',
            'employee_name': 'John Smith',
            'employee_role': 'Administrator'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Success', response.get_data(as_text=True))

        mock_save_employee.assert_called_once_with({
            'employee_id': '001',
            'employee_name': 'John Smith',
            'employee_role': 'Administrator'
        })

    @patch('employee.save_employee')
    def test_save_employee_missing_fields(self, mock_save_employee):
        
        response = self.app.post('/employee', json={
            'employee_name': 'John Smith'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Input', response.get_data(as_text=True))

        mock_save_employee.assert_not_called()  

    @patch('employee.get_employee')
    def test_save_employee_not_found(self, mock_get_employee):
        mock_get_employee.return_value = None 
        response = self.app.get('/employee/001')  
        self.assertEqual(response.status_code, 404)  
        self.assertIn('Employee not found', response.get_data(as_text=True))

        mock_get_employee.assert_called_once_with('001')

if __name__ == '__main__':
    unittest.main()
