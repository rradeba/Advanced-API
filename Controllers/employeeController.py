from flask import jsonify, request
from Models.employee import Employee
from extensions import db

def save_employee():
    data = request.get_json()
    new_employee = Employee(
        employee_id=data['employee_id'],
        employee_name=data['employee_name'],
        employee_position=data['employee_position']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": "Employee saved"}), 201

def get_employee():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    employees = Employee.query.paginate(page=page, per_page=per_page, error_out=False)

    response = { 
        'employees': [
            {
                'employee_id': employee.employee_id,  
                'employee_name': employee.employee_name,  
                'employee_position': employee.employee_position  
            } for employee in employees.items  
        ],
        'total': employees.total,       
        'pages': employees.pages,        
        'current_page': employees.page   
    }
  
    return jsonify(response), 200
