from flask import Blueprint, jsonify, request
from flask import Flask
import requests
import node 
import transaction
import blockchain
import json
import block
from argparse import ArgumentParser
from flask import abort

total_nodes=3

rest_api = Blueprint('rest_api', __name__)

# app = Flask(__name__)

parser = ArgumentParser()
required = parser.add_argument_group()
required.add_argument('-p',type=str,required=True)
args=parser.parse_args()
port=args.p

#my_port = main.port
my_node = node.Node(bootstrap_addr='localhost',bootstrap_port='5000',ip='localhost',port=port)
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
    bal = my_node.balance() #edo prepei na to pairnei apo to ring
    return jsonify({'balance':bal}),200

@rest_api.route('/send_transaction',methods=['POST'])
def send_transaction():
    if request.form.get('stake_flag') == 'False' :
        id = request.form['id']
        print('trans: ',request.form['message'], "from node with port", request.form['sender'], " to node ", id)
        my_node.create_transaction(request.form['sender'],id,request.form['message'], False)
        return jsonify(status=200)
    else: #stake
        print('stake trans')
        my_node.stake(request.form['id'], request.form['stake'])
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
        block[str(i)] = transaction.message
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
    if (my_node.validate_transaction(trans)):
    #if trans.verify_signature(): #edo theloume if validate_transaction
        print("Valid transaction")
        return (jsonify(),200)
    else:
        return (jsonify(),400)
    # print(trans.to_dict())
    # if transaction.verify_signature2(request.form["sender_address"],request.form["transaction_id"],request.form["signature"]): 
    #     print("valid transaction")
    #     return 200

@rest_api.route('/receive_transaction',methods=['POST'])
def receive_transaction() :
    stake = request.form["stake"]
    print("This is a stake transaction ", str(stake))
    trans = transaction.Transaction(request.form["sender_address"],request.form["nonce"],request.form["receiver_address"],request.form["message"],request.form["signature"],request.form["transaction_id"],stake=request.form["stake"])
    my_node.add_transaction(trans)
    return (jsonify(),200)

@rest_api.route('/broadcast_block',methods=['POST'])
def valid_block():
    prev_hash=request.form['previous_hash']
    validator = request.form['validator']
    print("I received the validator data from node ", validator)
    my_node.validate_block(prev_hash, validator)
    return jsonify(status=200)

@rest_api.route('/receive_block',methods=['POST'])
def receive_block():
    #block_hash = request.form['block_hash']
    #print("block hash ok")
    #previous_hash=request.form['previous_hash']
    #print("previous hash okay")
    my_validator = request.form['my_validator']
    validator_id = request.form['validator_id']
    #print("block hash is ", block_hash, " and previous hash is ", previous_hash)
    #if (validator_id == my_validator and block_hash == previous_hash):
    if (validator_id == my_validator):
        print("Block has been validated")
        return jsonify(status=200)
    else:
        print("Block couldn't be validated")
        abort(400)

"""
TO DO :
-main gia 5-10 nodes
-ta stake transactions metrane sto block?
-den exoume generate_wallet
-genesis block kai validate_chain?
-dialegoyme panta ton 2 gia validator (mallon exei na kanei me to hash pou leo pano)
-h /receive block den elegxei ta previous hash
"""