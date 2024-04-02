import blockchain
import time 
import json
import Crypto
from Crypto.Hash import SHA256



class Block:
    def __init__(self,index,validator):
        self.previous_hash = None
        self.timestamp = time.time()
        self.validator = validator
        self.index = index 
        self.transactions_list = []
        self.capacity = 100
        self.current_hash = None
        self.fees = 0

    def myHash(self): 
        """
        Calculates block hash and assigns it to current_hash.
        """
        hash_message = {
        'previous_hash': self.previous_hash,
        'timestamp': self.timestamp,
        'index': self.index
        }
        block_dump = json.dumps(hash_message.__str__())
        hash1 = hash.SHA256.new(block_dump.encode("ISO-8859-1")).hexdigest()
        self.current_hash = hash1
        return hash1
    
    def check_and_add_transaction_to_block(self,transaction):
        """
        Appends transaction to block, then checks if block reached capacity.
        """
        self.transactions_list.append(transaction)
        if self.capacity > len(self.transactions_list):
            return True
        else:
            print("Block is at capacity !!!")
            return False