from flask import Blueprint, jsonify, request
from flask import Flask
import node 
import transaction
import blockchain
import json
import block

rest_api = Blueprint('rest_api', __name__)

# app = Flask(__name__)

my_node = node.Node()
bc = blockchain.Blockchain()

block1 = block.Block(1, 69)
block1.transactions_list = ["first"]
block2 = block.Block(2, 420)
block2.transactions_list = ["second", "third"]

bc.add_to_blockchain(block1)
bc.add_to_blockchain(block2)

@rest_api.route('/balance',methods=['GET'])
def balance():
    bal = my_node.wallet.unspent
    return jsonify({'balance':bal}),200

@rest_api.route('/send_transaction',methods=['POST'])
def send_transaction():
    id = request.form['id']
    if request.form.get('message') :
        my_node.create_transaction(id,0,request.form['message'])
        print('message trans : ',request.form['message'])
    elif request.form.get('amount') :
        print('coin trans')
    else :
        print('stake trans')
    return jsonify(status=200)

@rest_api.route('/view_block',methods=['GET'] )
def view_block():
    block = {}
    last_block = bc.blocks_of_blockchain[-1]
    transactions_list = last_block.transactions_list
    validator = last_block.validator
    for i, transaction in enumerate(transactions_list):
        block[str(i)] = transaction #testing, kanonika thelei transaction.to_dict()
    return jsonify(block=block, validator=validator, status=200)

# @rest_api.route('/view_block',methods=['GET'] ) #this works for a block
# def view_block():
#     #counter = 0
#     #block = {}
#     block = my_node.current_block.to_dict()
#     print(block)
#     return jsonify(status=200)

@rest_api.route('/validate_transaction',methods=['POST'])
def validate_transaction() :
    print(request.form)
    print(100)
    trans = transaction.Transaction(request.form["sender_address"],request.form["nonce"],request.form["receiver_address"],request.form["amount"],request.form["message"],request.form["type"],request.form["signature"],request.form["transaction_id"])
    print(trans.transaction_id)
    if trans.verify_signature():
        print("valid transaction")
        return jsonify(),200
    # print(trans.to_dict())
    # if transaction.verify_signature2(request.form["sender_address"],request.form["transaction_id"],request.form["signature"]): 
    #     print("valid transaction")
    #     return 200
    
@rest_api.route('/receive_transaction',methods=['POST'])
def receive_transaction() :
    trans = transaction.Transaction(request.form["sender_address"],request.form["nonce"],request.form["receiver_address"],request.form["amount"],request.form["message"],request.form["type"],request.form["signature"],request.form["transaction_id"])
    # my_node.add_transaction(trans)
    print("successfuly received")
    return jsonify(status=200)

@rest_api.route('/receive_valid_block',methods=['POST'])
def valid_block():
    prev_hash=request.form['hash']
    print("block validated")
    return jsonify(status=200)


#app.run(port=5000)