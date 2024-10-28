import unittest
from unittest import mock
from app import create_app  
from flask import jsonify
from extensions import db 
from Controllers.employeeController import save_employee, get_employee


class TestEmployee(unittest.TestCase):
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

    @mock.patch('Controllers.employeeController.save_employee')  
    def test_create_employee(self, mock_save_employee):
        response = self.client.post('/employee/', json={
            'employee_id': 1,
            'employee_name': 'Jane Doe',
            'employee_position': 'Administrator'
        })
        
        print(mock_save_employee)
        print(response.get_json())
        print("Response JSON:", response.get_json())
        print("Mock was called:", mock_save_employee.called)
        print("Mock call args:", mock_save_employee.call_args)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('Employee saved', response.get_data(as_text=True))

    def test_create_employee_invalid_input(self):
        response = self.client.post('/employee/', json={
            'employee_name': 'Jane Doe'  
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    @mock.patch('Controllers.employeeController.get_employee')  
    def test_get_employee_not_found(self, mock_get_employee):
        mock_get_employee.return_value = jsonify({"message": "Employee not found"}), 404
        response = self.client.get('/employee/999')
        self.assertIn('Employee not found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
