from flask import jsonify, request
from Models.product import Product 
from extensions import db

def save_product():
   
    data = request.get_json()
    new_product = Product(
        product_id=data['product_id'],
        product_name=data['product_name'],
        product_price=data['product_price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product saved"}), 201

def get_product():
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)

   
    response = {
        'products': [
            {
                'product_id': product.product_id, 
                'product_name': product.product_name,  
                'product_price': product.product_price 
            } for product in products.items
        ],
        'total': products.total,          
        'pages': products.pages,         
        'current_page': products.page     
    }
    
    
    return jsonify(response), 200
