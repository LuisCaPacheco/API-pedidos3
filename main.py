from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)

@app.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(customer_name=data['customer_name'], product_name=data['product_name'], payment_status='pending')
    db.session.add(new_order)
    db.session.commit()

    payment_response = make_payment(data['payment_method'], data['product_price'])

    if payment_response['status'] == 'success':
        new_order.payment_status = 'success'
    else:
        new_order.payment_status = 'failed'

    db.session.commit()

    return json