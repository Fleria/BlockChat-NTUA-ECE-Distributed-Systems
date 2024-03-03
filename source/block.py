import blockchain
import time 
import json
from Crypto.Hash import SHA256

class Block:
    def __init__(self):
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.hash = None
        self.validator = None
        self.index = None #poio block einai 1o, 2o...
        self.transactions_list = []

    def myHash(): #calculates hash using sha
        hash_message = {} # json me ta stoixeia tou block
        block_dump = json.dumps(block_list.__str__())
        return SHA256.new(block_dump.encode("ISO-8859-1")).hexdigest()
    
    def add_transaction(transaction, blockchain): #adds transaction to block
        self.transactions_list.append(transaction)
        # check for capacity of the block