from flask import jsonify, request
from Models.product import Product 
from extensions import db

def save_product():
   
    data = request.get_json()
    if not data or not all(k in data for k in ('product_id', 'product_name','product_price')):
        return jsonify({"message": "Invalid input"}), 400
    
    new_product = Product(
        product_id=data['product_id'],
        product_name=data['product_name'],
        product_price=data['product_price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product saved"}), 201

def get_product(product_id):
    
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"message": "Product not found"}), 404

   
    response = {

            
                'product_id': product.product_id, 
                'product_name': product.product_name,  
                'product_price': product.product_price 
            
        }
    
    return jsonify(response), 200
