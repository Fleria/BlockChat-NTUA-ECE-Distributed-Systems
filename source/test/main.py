from flask import Flask, jsonify, request, render_template
#from flask_cors import CORS
import json
import block
import node
import blockchain
import wallet
import transaction
from api_test import rest_api, my_node

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

app.run(port=5000)
#my_node.create_transaction( 0, 10, ' diaroia')