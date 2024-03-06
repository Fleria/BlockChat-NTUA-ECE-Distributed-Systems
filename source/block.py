import blockchain
import time 
import json
from Crypto.Hash import SHA256

class Block:
    def __init__(self, previous_hash):
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.validator = None
        self.index = None #poio block einai 1o, 2o...
        self.transactions_list = []
        self.capacity = 0
        self.current_hash = None

    def myHash(self): #calculates hash using sha, pairnei parametro self 
        hash_message = {self.previous_hash, self.timestamp, self.index} # dictionary me ta stoixeia tou block
        block_dump = json.dumps(hash_message.__str__()) #to kanoume json
        hash = SHA256.new(block_dump.encode("ISO-8859-1")).hexdigest()
        self.current_hash = hash
        return hash
    
    def add_transaction(self, transaction): #adds transaction to block, returns false if block is full
        if self.capacity <= len(self.transactions_list):
            self.transactions_list.append(transaction)
            return True
        else:
            print("Block is at capacity !!!")
            return False
    
