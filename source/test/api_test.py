from flask import Blueprint, jsonify, request
from flask import Flask
import requests
import node 
import transaction
import blockchain
import json
import block

total_nodes=3

rest_api = Blueprint('rest_api', __name__)

# app = Flask(__name__)

my_node = node.Node(bootstrap_addr='localhost',bootstrap_port='5000',ip='localhost')
# bc = blockchain.Blockchain()

# block1 = block.Block(1, 69)
# block1.transactions_list = ["first"]
# block2 = block.Block(2, 420)
# block2.transactions_list = ["second", "third"]

# bc.add_to_blockchain(block1)
# bc.add_to_blockchain(block2)


@rest_api.route('/register_to_ring', methods=['POST'])
def register_to_ring() :
    key = request.form["public_key"]
    address = request.form["address"]
    port = request.form["port"]
    id = len(my_node.ring)
    print("register node with address", address, port, "to ring of len" , id+1)
    my_node.register_node_to_ring(id,address,port,key,1000)

    if id == total_nodes-1 :
        for node in my_node.ring.values() :
            if node[0] !=0 and node[0]!=total_nodes-1 : #not bootstrap or final node
                url="http://"+ node[1] + ':'+node[2] +'/share_ring'
                data = {'ring': json.dumps(my_node.ring)}
                response = requests.post(url, data = data)
                if(response.status_code == 200) :
                    print("successful ring sharing for node ", id)
        return jsonify({'id': id, 'ring':my_node.ring}),200
    else : 
        return jsonify({'id':id}),200
    

@rest_api.route('/share_ring', methods=['POST'])
def share_ring():
    data = json.loads(request.form['ring'])
    my_node.ring=data
    #for node in my_node.ring.values() :
     #   print("now printing ring")
      #  print(node)
    #print(my_node.ring)
    return jsonify(),200


@rest_api.route('/balance',methods=['GET'])
def balance():
    bal = my_node.BCC
    return jsonify({'balance':bal}),200

@rest_api.route('/send_transaction',methods=['POST'])
def send_transaction():
    if request.form.get('message') :
        id = request.form['id']
        print('trans : ',request.form['message'], " to node ", id)
        my_node.create_transaction(id,request.form['sender'],request.form['message'])
    # elif request.form.get('amount').isdigit() : #coin
    #     print('coin trans', request.form['message'])
    #     my_node.create_transaction(id,request.form['amount'])
    else : #stake
        print('stake trans')
        my_node.stake(request.form['stake'])
    return jsonify(status=200)

@rest_api.route('/view_block',methods=['GET'] )
def view_block():
    block = {}
    if(len(my_node.blockchain.blocks_of_blockchain) == 0):
        print("No block has been validated yet!")
        return jsonify(status=400)
    last_block = my_node.blockchain.blocks_of_blockchain[-1]
    transactions_list = last_block.transactions_list
    validator = last_block.validator
    index = last_block.index
    for i, transaction in enumerate(transactions_list):
        block[str(i)] = transaction.message #testing, kanonika thelei transaction.to_dict()
    return jsonify(block=block,validator=validator, index=index, status=200)

# @rest_api.route('/view_block',methods=['GET'] ) #this works for a block
# def view_block():
#     #counter = 0
#     #block = {}
#     block = my_node.current_block.to_dict()
#     print(block)
#     return jsonify(status=200)

@rest_api.route('/validate_transaction',methods=['POST'])
def validate_transaction() :
    trans = transaction.Transaction(request.form["sender_address"],request.form["nonce"],request.form["receiver_address"],request.form["message"],request.form["signature"],request.form["transaction_id"])
    if trans.verify_signature(): #edo theloume if validate_transaction
        print("Valid transaction")
        return (jsonify(),200)
    # print(trans.to_dict())
    # if transaction.verify_signature2(request.form["sender_address"],request.form["transaction_id"],request.form["signature"]): 
    #     print("valid transaction")
    #     return 200
    
@rest_api.route('/receive_transaction',methods=['POST'])
def receive_transaction() :
    trans = transaction.Transaction(request.form["sender_address"],request.form["nonce"],request.form["receiver_address"],request.form["message"],request.form["signature"],request.form["transaction_id"])
    my_node.add_transaction(trans)
    print("successfuly received", trans.to_dict())
    return jsonify(),200

@rest_api.route('/receive_valid_block',methods=['POST'])
def valid_block():
    prev_hash=request.form['hash']
    print("block validated")
    return jsonify(status=200)


#app.run(port=5000)
"""
TO DO :
-na tsekaroume oti kanei balance sosta to ipoloipo
-na tsekaroume stake
-client gia 5-10 nodes
-main gia 5-10 nodes
-self.BCC vs wallet.unspent sto ring
-sender id? stin create transaction prepei na to pairnoume apo to port kai to ring
"""