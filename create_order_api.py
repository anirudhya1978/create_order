from flask import Flask, jsonify, request
from create_order import  create_order, create_shipment

app= Flask(__name__)

@app.route('/create_order', methods=['POST'])
def create_orders():
    customer_id = request.form.get('customer_id')
    order_items = request.form.get('order_item')
    order_value = request.form.get('order_value')
    shipper = request.form.get('shipper')
    order_id = create_order(customer_id,order_items, order_value)
    shipment_id = create_shipment(order_id, shipper)
    
    return jsonify({'Order Id':order_id,
                    'Shipment Id':shipment_id})

if __name__== '__main__':
    app.run(debug=False,host='0.0.0.0')
