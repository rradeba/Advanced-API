from flask import jsonify, request
from Models.order import Order
from Models.order import Order
from Models.order import Order
from Models.order import Order
from extensions import db

def save_order():
    data = request.get_json()
    new_order = Order(
        customer_id=data['customer_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        total_price=data['total_price']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order saved"}), 201

def get_order():
 
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    
    orders = Order.query.paginate(page=page, per_page=per_page, error_out=False)

   
    response = {
        'orders': [
            {
                'id': order.order_id,
                'customer_id': order.customer_id,
                'product_id': order.product_id,
                'quantity': order.quantity,
                'total_price': order.total_price
            } for order in orders.items
        ],
        'total': orders.total,          
        'pages': orders.pages,         
        'current_page': orders.page    
    }
    
    
    return jsonify(response), 200
