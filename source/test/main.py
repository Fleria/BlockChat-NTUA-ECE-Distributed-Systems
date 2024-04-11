from flask import Flask, jsonify, request, render_template
import requests
import json
from argparse import ArgumentParser
import block
import node
import blockchain
import wallet
import transaction
from api_test import rest_api, my_node

app = Flask(__name__)
app.register_blueprint(rest_api)

genesis_transaction = transaction.Transaction(0, 0, 0, '5000')

total_nodes = 5

if __name__ == '__main__':
    parser = ArgumentParser()
    required = parser.add_argument_group()
    required.add_argument('-p',type=str,required=True)
    args=parser.parse_args()
    port=args.p
    if port == '5000' :#bootstrap node
        print("bootstrap node entered")
        my_node.id=0
        my_node.port=port
        my_node.register_node_to_ring(0,'localhost','5000',my_node.wallet.address,1000*total_nodes)
        print("bootstrap node registered")
        #genesis
        my_node.current_block.transactions_list.append(genesis_transaction)
        my_node.blockchain.blocks_of_blockchain.append(my_node.current_block)
        print("Current length of blockchain is", len(my_node.blockchain.blocks_of_blockchain))
        my_node.current_block = block.Block(1)
        
        app.run(port=port)

    else: #other nodes
        print("node", port, "entered")
        my_node.port=port
        endpoint = 'http://' + my_node.bootstrap_addr + ':' + my_node.bootstrap_port + '/register_to_ring'
        info = {
                'public_key':my_node.wallet.address,
                'address':'localhost',
                'port':port,
                'genesis_transaction': genesis_transaction,
                }
        response = requests.post(endpoint,info)
        res = response.json()
        my_node.id=res['id']
        print("node registered with id ", my_node.id)
        if 'ring' in res : #the last node to enter
            my_node.ring=res['ring']
            my_node.current_block.transactions_list.append(genesis_transaction)
            my_node.blockchain.blocks_of_blockchain.append(my_node.current_block)
            print("the length of my genesis block is", len(my_node.current_block.transactions_list))
            my_node.current_block = block.Block(1)
        
        app.run(port=port)