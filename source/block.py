import blockchain
import time 
import json
from Crypto.Hash import SHA256

capacity = 3

class Block:
    def __init__(self,capacity,index,validator):
        self.previous_hash = None
        self.timestamp = time.time()
        self.validator = validator
        self.index = index #poio block einai 1o, 2o...
        self.transactions_list = []
        self.capacity = capacity
        self.current_hash = None

    def myHash(self): #calculates hash using sha, pairnei parametro self 
        hash_message = {
        'previous_hash': self.previous_hash,
        'timestamp': self.timestamp,
        'index': self.index
        }
        # dictionary me ta stoixeia tou block
        block_dump = json.dumps(hash_message.__str__()) #to kanoume json
        hash = SHA256.new(block_dump.encode("ISO-8859-1")).hexdigest()
        self.current_hash = hash
        return hash
    
    def check_and_add_transaction_to_block(self,transaction):
        self.transactions_list.append(transaction)
        if self.capacity < len(self.transactions_list):
            return True
        else:
            print("Block is at capacity !!!")
            return False