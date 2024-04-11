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

total_nodes=5

rest_api = Blueprint('rest_api', __name__)

parser = ArgumentParser()
required = parser.add_argument_group()
required.add_argument('-p',type=str,required=True)
args=parser.parse_args()
port=args.p


my_node = node.Node(bootstrap_addr='localhost',bootstrap_port='5000',ip='localhost',port=port)


@rest_api.route('/register_to_ring', methods=['POST'])
def register_to_ring() :
    key = request.form["public_key"]
    address = request.form["address"]
    port = request.form["port"]
    #genesis_transaction = request.form["genesis_transaction"]
    id = len(my_node.ring)
    print("Registering node with address", address, port, "to ring of length" , id+1)
    my_node.register_node_to_ring(id,address,port,key,1000)
    my_node.ring[my_node.wallet.public_key][3] -= 1000

    if id == total_nodes-1 : #finished with node adding
        for node in my_node.ring.values() :
            if node[0] !=0 and node[0]!=total_nodes-1 : #not bootstrap or final node
                url="http://"+ node[1] + ':'+node[2] +'/share_ring'
                blockchain=json.dumps(my_node.blockchain.to_dict())
                print("starting blockchain is ",blockchain)               
                data = {
                    'ring': json.dumps(my_node.ring),
                    'blockchain': blockchain
                    }
                response = requests.post(url, data = data)
                #if(response.status_code == 200) :
                    #print("successful ring sharing for node ", node[0])
        return jsonify({'id': id, 'ring':my_node.ring, 'blockchain':blockchain}),200
    else : 
        return jsonify({'id':id}),200
    

@rest_api.route('/share_ring', methods=['POST'])
def share_ring():
    ring = json.loads(request.form['ring'])
    blockch=json.loads(request.form['blockchain'])
    print("received blockchain is " ,blockch)
    print("built blockchain is ")
    for bloc in blockch.values() :
        newbl=block.Block(bloc['index'],bloc['previous_hash'])
        newbl.current_hash=bloc['current_hash']
        newbl.validator=bloc['validator']
        #build block transaction list
        print(newbl.to_dict1(),"\n")
        my_node.blockchain.add_to_blockchain(newbl) #adam
        my_node.current_block = block.Block(1, newbl.current_hash) #adam
        print("the hash of my new block is", newbl.current_hash) #adam
    my_node.ring=ring
    return jsonify(),200
    # url="http://localhost:"+my_node.port +'/receive_block'
    # response=requests.post(url,{'hash':1,'validator':0})
    # if response.status_code==200 :
    #     return jsonify(),200

@rest_api.route('/balance',methods=['GET'])
def balance():
    bal = my_node.balance()
    return jsonify({'balance':bal}),200

@rest_api.route('/send_transaction',methods=['POST'])
def send_transaction():
    if request.form.get('stake_flag') == 'False' :
        id = request.form['id']
        print('I am sending a trans: ',request.form['message'], "from node with port", request.form['sender'], " to node ", id)
        if my_node.create_transaction(request.form['sender'],id,request.form['message'], False) :
            return jsonify(),200
        else :
            return jsonify(),400
    else: #stake
        print('Stake trans')
        if my_node.stake(request.form['id'],request.form['id'], request.form['stake']):
            return jsonify(),200
        else :
            return jsonify(),400

@rest_api.route('/view_block', methods=['GET'])
def view_block():
    block = {}
    if len(my_node.blockchain.blocks_of_blockchain) == 0:
        print("No block has been validated yet!")
        return jsonify(status=400)

    last_block = my_node.blockchain.blocks_of_blockchain[-1]
    transactions_list = last_block.transactions_list
    validator = last_block.validator
    index = last_block.index
    timestamp = last_block.timestamp
    capacity = last_block.capacity
    fees = last_block.fees
    previous_hash = last_block.previous_hash
    
    block_data = {
        'Block_validator': validator,
        'Block_index': index,
        'List_of_transactions': [],
        'Timestamp': timestamp,
        'Capacity': capacity,
        'Fees': fees,
        'Previous_hash': previous_hash
    }

    if previous_hash == 1: #genesis block adam
        transaction_info = {
            "Sender node": 0,
            "Receiver node": 0,
            "Transaction message": 1000*total_nodes
        }
        transaction_str = "{" + ", ".join([f"{key}: {value}" for key, value in transaction_info.items()]) + "}"
        block_data['List_of_transactions'].append(transaction_str)

    else:
        for i, transaction in enumerate(transactions_list):
            sender_address = transaction.sender_address
            receiver_address = transaction.receiver_address
            for key, value in my_node.ring.items():
                if key ==  sender_address:
                    sender_node = value[0]
                if key == receiver_address:
                    receiver_node = value[0]
            transaction_info = {
                "Sender node": f"{sender_node}",
                "Receiver node": f"{receiver_node}",
                "Transaction message": f"{transaction.message}"
            }
            transaction_str = "{" + ", ".join([f"{key}: {value}" for key, value in transaction_info.items()]) + "}"
            block_data['List_of_transactions'].append(transaction_str)

    return jsonify(block=block_data, status=200)


@rest_api.route('/validate_transaction',methods=['POST'])
def validate_transaction() :
    trans = transaction.Transaction(request.form["sender_address"],request.form["nonce"],request.form["receiver_address"],request.form["message"],request.form["signature"],request.form["transaction_id"])
    if (my_node.validate_transaction(trans)):
        print("Valid transaction")
        return (jsonify(),200)
    else:
        return (jsonify(),400)

@rest_api.route('/receive_transaction',methods=['POST'])
def receive_transaction() :
    stake = request.form["stake"]
    if stake=='True' : 
        print("This is a stake transaction ")
    trans = transaction.Transaction(request.form["sender_address"],request.form["nonce"],request.form["receiver_address"],request.form["message"],request.form["signature"],request.form["transaction_id"],stake=request.form["stake"])
    if my_node.add_transaction(trans) == 205 :
        return jsonify(),205
    return (jsonify(),200)

@rest_api.route('/broadcast_block',methods=['POST'])
def broadcast_block():
    prev_hash=request.form['hash']
    #print(prev_hash)
    validator = request.form['validator_id']
    #print("validator is", validator)
    print("I received the validator data from node ", validator)
    my_node.validate_block(prev_hash, validator)
    return jsonify(status=200)

@rest_api.route('/receive_block',methods=['POST'])
def receive_block():
    validator=request.form['validator']
    hash=request.form['hash']
    my_node.current_block.current_hash=hash
    my_node.current_block.validator=validator
    my_node.blockchain.add_to_blockchain(my_node.current_block)
    index=my_node.current_block.index+1
    my_node.current_block=block.Block(index)
    my_node.current_block.previous_hash=hash
    print("Valid block in the blockchain")
    return jsonify(),200

@rest_api.route('/select_validator', methods=['GET'])
def select_validator():
    validator=my_node.select_validator()
    print("The validator is ", validator)
    return jsonify ({'validator_id':validator}),200

@rest_api.route('/validate_block',methods=['GET'])
def validate_block():
    hash=my_node.calculate_block_hash()
    return jsonify({'hash':hash}),200

@rest_api.route('/blockchain_length',methods=['GET'])
def blockchain_length():
    length = len(my_node.blockchain.blocks_of_blockchain)
    return jsonify({'blocks':length}),200