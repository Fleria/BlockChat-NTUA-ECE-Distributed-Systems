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


total_nodes = 10

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
        genesis_transaction = transaction.Transaction(0, 0, 0, '5000')
        my_node.current_block.transactions_list.append(genesis_transaction)
        hash=my_node.current_block.myHash1()
        my_node.current_block.current_hash=hash
        my_node.blockchain.blocks_of_blockchain.append(my_node.current_block)
        print("Current length of blockchain is", len(my_node.blockchain.blocks_of_blockchain))
        my_node.current_block = block.Block(1,hash)
        print("the hash of my new block is", hash)
        app.run(port=port)

    else: #other nodes
        print("node", port, "entered")
        my_node.port=port
        endpoint = 'http://' + my_node.bootstrap_addr + ':' + my_node.bootstrap_port + '/register_to_ring'
        info = {
                'public_key':my_node.wallet.address,
                'address':'localhost',
                'port':port,
                }
        response = requests.post(endpoint,info)
        res = response.json()
        my_node.id=res['id']
        print("node registered with id ", my_node.id)
        if 'ring' in res : #the last node to enter
            my_node.ring=res['ring']
        if 'blockchain' in res: 
            print("blockchain is ", res['blockchain'])
            for bloc in json.loads(res['blockchain']).values() :
                newbl=block.Block(bloc['index'],bloc['previous_hash'])
                newbl.current_hash=bloc['current_hash']
                newbl.validator=bloc['validator']
                #build block transaction list
                print(newbl.to_dict1(),"\n")
                my_node.blockchain.add_to_blockchain(newbl) #adam
                my_node.current_block = block.Block(1, newbl.current_hash) #adam
                print("the hash of my new block is", newbl.current_hash) #adam
            # my_node.current_block.transactions_list.append(genesis_transaction)
            # my_node.blockchain.blocks_of_blockchain.append(my_node.current_block)
            # print("the length of my genesis block is", len(my_node.current_block.transactions_list))
            # my_node.current_block = block.Block(1)
        # if port == '5002': #adam
        #     print("the length of my blockchain is", len(my_node.blockchain.blocks_of_blockchain))
        #     genesis_transaction = transaction.Transaction(0, 0, 0, '5000')
        #     my_node.current_block = block.Block(1,1)
        #     my_node.current_block.transactions_list.append(genesis_transaction)
        #     hash=my_node.current_block.myHash1() #i myHash1 einai kainouria sinartisi pou hasharei mono to index gia eukolia
        #     my_node.current_block.current_hash=hash
        #     my_node.blockchain.blocks_of_blockchain.append(my_node.current_block)
        #     my_node.current_block = block.Block(1,hash)
        #     print("the hash of my new block is", hash)
        app.run(port=port)