from flask import jsonify, request
from Models.order import Order
from extensions import db

def save_order():
    data = request.get_json()
    if not data or not all(k in data for k in ('order_id', 'order_quantity','total_price')):
        return jsonify({"message": "Invalid input"}), 400
    
    new_order = Order(
        order_id=data['order_id'],
        order_quantity=data['order_quantity'],
        total_price=data['total_price']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order saved"}), 201

def get_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"message": "Order not found"}), 404

   
    response = {
        'order_id': order.order_id,
        'quantity': order.order_quantity,
        'total_price': order.total_price
    }
    
    return jsonify(response), 200
