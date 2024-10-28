from flask import jsonify, request
from Models.production import Production
from extensions import db

def save_production():
    
    data = request.get_json()
    if not data or not all(k in data for k in ('production_id', 'production_quantity')):
        return jsonify({"message": "Invalid input"}), 400
   
    new_production = Production(
        production_id=data['production_id'],
        production_quantity=data['production_quantity']
    )
    db.session.add(new_production)
    db.session.commit()
    return jsonify({"message": "Production saved"}), 201

def get_production(production_id):
    
    production = Production.query.get(production_id)
    if production is None:
        return jsonify({"message": "Production not found"}), 404

    return jsonify({
        'production_id': production.production_id,
        'production_quantity': production.production_quantity
    }), 200 




