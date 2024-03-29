from flask import Blueprint, jsonify, request
import node
import transaction
import requests

total_nodes = 5

my_node = node.Node()

rest_api = Blueprint('rest_api', __name__)

@rest_api.route('/register_to_ring', methods=['POST'])
def register_to_ring() :
    "call from new nodes to bootstrap" 
    key = request.form["public_key"]
    address = request.form["address"]
    port = request.form["port"]
    id = len(my_node.ring)
    my_node.register_node_to_ring(id,address,port,key)

    if id == total_nodes :
        for node in my_node.ring :
            url="http://"+ address + ':'+port +'/share_ring'
            response = requests.post(url, data = my_node.ring)
            if(response.status_code == 200) :
                print("successful ring sharing for node ", id)
    
    return jsonify({'id': id}, status = 200)

@rest_api.route('/validate_transaction',methods=['POST'])
def validate_transaction() :
    trans = transaction.Transaction(request.form["sender_address"],request.form["nonce"],request.form["receiver_address"],request.form["amount"],request.form["message"],request.form["type"])
    if my_node.validate_transaction(trans): 
        return jsonify(status=200)
    
@rest_api.route('/receive_transaction',methods=['POST'])
def receive_transaction() :
    trans = transaction.Transaction(request.form["sender_address"],request.form["nonce"],request.form["receiver_address"],request.form["amount"],request.form["message"],request.form["type"])
    my_node.add_transaction(trans)
    return jsonify(status=200)