from flask import Blueprint, jsonify, request
import node
import transaction
import requests

total_nodes = 2

my_node = node.Node()

rest_api = Blueprint('rest_api', __name__)

@rest_api.route('/register_to_ring', methods=['POST'])
def register_to_ring() :
    #call from new nodes to bootstrap
    key = request.form["public_key"]
    address = request.form["address"]
    port = request.form["port"]
    id = len(my_node.ring)
    my_node.register_node_to_ring(id,address,port,key,1000)

    if id == total_nodes-1 :
        for node in my_node.ring :
            url="http://"+ node[1] + ':'+node[2] +'/share_ring'
            response = requests.post(url, data = my_node.ring)
            if(response.status_code == 200) :
                print("successful ring sharing for node ", id)
    
    return jsonify({'id': id}),200

@rest_api.route('/share_ring', methods=['POST'])
def share_ring():
    print(request)


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

@rest_api.route('/receive_valid_block',methods=['POST'])
def valid_block():
    prev_hash=request.form['hash']
    my_node.blockchain.add_hash(prev_hash)
    return jsonify(status=200)

@rest_api.route('/balance')
def balance():
    bal=my_node.balance()
    return jsonify({'balance':bal},status=200)

@rest_api.route('/send_transaction',methods=['POST'])
def send_transaction():
    id = request.form['id']
    if request.form.get('message') :
        my_node.create_transaction(id,0,request.form['message'])
    elif request.form.get('amount') :
        my_node.create_transaction(id,request.form['amount'],'')
    else :
        my_node.stake(request.form.get['stake'])
    return jsonify(status=200)

@rest_api.route('/view_block',methods=['GET'] )
def view_block():
    counter = 0
    block = {}
    for transaction in my_node.blockchain[-1].transaction_list :
        block[str(counter)] = transaction.to_dict()
        counter+=1
    return jsonify(block,status=200)



