from flask import jsonify, request
from Models.production import Production
from extensions import db

def save_production():
    
    data = request.get_json()
    new_production = Production(
        production_id=data['production_id'],
        production_quantity=data['production_quantity'],
        production_date=data['production_date']
    )
    db.session.add(new_production)
    db.session.commit()
    return jsonify({"message": "Production saved"}), 201

def get_production():
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    
    productions = Production.query.paginate(page=page, per_page=per_page, error_out=False)

   
    response = { 
        'production': [
            {
                'production_id': production.production_id, 
                'production_quantity': production.production_quantity,  
                'production_date': production.production_date, 
            } for production in productions.items  
        ],
        'total': productions.total,        
        'pages': productions.pages,        
        'current_page': productions.page   
    }
    
    return jsonify(response), 200



