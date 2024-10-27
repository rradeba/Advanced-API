import unittest
from unittest import mock
from app import create_app  
from extensions import db
from Models.employee import Employee  # Make sure the path is correct
from Controllers.employeeController import save_employee, get_employee 

class TestEmployee(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')  
        self.app_context = self.app.app_context()
        self.app_context.push()

        with self.app.app_context():
            db.create_all()  # Create the tables

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    @mock.patch('Controllers.employeeController.save_employee')  
    def test_create_employee_success(self, mock_save_employee):
        response = self.client.post('/employee/', json={
            'employee_id': 1,
            'employee_name': 'John Smith',
            'employee_position': 'Administrator'
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('Success', response.get_data(as_text=True))

    
        employee = Employee.query.get(1)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.employee_name, 'John Smith')
        
        
        mock_save_employee.assert_called_once_with({
            'employee_id': 1,
            'employee_name': 'John Smith',
            'employee_position': 'Administrator'
        })

    @mock.patch('Controllers.employeeController.save_employee')  
    def test_save_employee_missing_fields(self, mock_save_employee):
        response = self.client.post('/employee/', json={
            'employee_name': 'John Smith'  
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Input', response.get_data(as_text=True))

        
        mock_save_employee.assert_not_called()  

    @mock.patch('Controllers.employeeController.get_employee')  
    def test_get_employee_not_found(self, mock_get_employee):
        mock_get_employee.return_value = None 
        
        response = self.client.get('/employee/1')  
        
        self.assertEqual(response.status_code, 404)  
        self.assertIn('Employee not found', response.get_data(as_text=True))

        
        mock_get_employee.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
