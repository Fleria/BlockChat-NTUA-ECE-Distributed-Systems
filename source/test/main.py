from flask import Flask, jsonify, request, render_template
#from flask_cors import CORS
import requests
import json
from argparse import ArgumentParser
import block
import node
import blockchain
import wallet
import transaction
from api_test import rest_api, my_node
import sys
import subprocess
import signal

# for i in range(10) :
#     my_node.create_transaction(i,10+i,'diaroia'+ str(i))
# my_node.blockchain.add_to_blockchain(my_node.current_block)
# counter = 0
# block = {}
# for transacti in my_node.blockchain.blocks_of_blockchain[-1].transactions_list :
#         print(transacti.to_dict())
#         print(transacti.verify_signature())
#         #print(json.dumps(transacti.to_dict().__str__()))
#         counter+=1



app = Flask(__name__)
app.register_blueprint(rest_api)
#blockchain = Blockchain()

# def terminate_processes(signum, frame):
#     print("Terminating processes...")
#     client_process.terminate()
#     sys.exit(0)

if __name__ == '__main__':
    parser = ArgumentParser()
    required = parser.add_argument_group()
    required.add_argument('-p',type=str,required=True)
    args=parser.parse_args()
    port=args.p
    #client_process = subprocess.Popen(['cmd', '/k', 'python3', 'client.py', '-p', port], creationflags=subprocess.CREATE_NEW_CONSOLE)
    if port == '5000' :#bootstrap node
        print("bootstrap node entered")
        my_node.id=0
        my_node.port=port
        my_node.register_node_to_ring(0,'localhost','5000',my_node.wallet.address,1000)
        print("bootstrap node registered")
        #genesis
        for key, value in my_node.ring.items():
            if value[0]==my_node.current_validator:
                validator_key = key
        print("Appending genesis transaction")
        genesis_transaction = transaction.Transaction(0, 0, validator_key, '5000')
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
                'port':port
                }
        response = requests.post(endpoint,info)
        res = response.json()
        my_node.id=res['id']
        print("node registered with id ", my_node.id)
        if 'ring' in res : 
            my_node.ring=res['ring']
        #genesis
        for key, value in my_node.ring.items():
            print("my node validator is", my_node.current_validator)
            print("i have a ring with id", value[0])
            if value[0]==my_node.current_validator:
                validator_key = key
        print("Appending genesis transaction")
        genesis_transaction = transaction.Transaction(0, 0, 0, '5000')
        my_node.current_block.transactions_list.append(genesis_transaction)
        my_node.blockchain.blocks_of_blockchain.append(my_node.current_block)
        print("Current length of blockchain is", len(my_node.blockchain.blocks_of_blockchain))   
        my_node.current_block = block.Block(1)
        
        app.run(port=port)