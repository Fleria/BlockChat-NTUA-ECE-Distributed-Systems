from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

import block
import node
import blockchain
import wallet
import transaction

app = Flask(_name_)
CORS(app)
blockchain = Blockchain()