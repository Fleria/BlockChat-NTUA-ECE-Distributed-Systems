import block
import wallet
import transaction
import blockchain
import Crypto
import Crypto.Random
import hashlib
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
import requests
from threading import Lock
import random
import time
import json

class Block:
    def __init__(self,index,previous_hash=1):
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.validator = 0 #debugging, None
        self.index = index 
        self.transactions_list = []
        self.capacity = 2
        self.current_hash = None
        self.fees = 0

    def to_dict(self):
        dict = {
            "validator" : self.validator,
            "transactions_list": self.transactions_list,
            "previous_hash": self.previous_hash
        }
        return dict  

    def myHash(self): 
        """
        Calculates block hash and assigns it to current_hash.
        """
        hash_message = {
        'previous_hash': self.previous_hash,
        'timestamp': self.index,
        'index': self.index,
        'transactions_list': self.transactions_list
        }
        print("timestamp is")
        print(self.timestamp)
        block_dump = json.dumps(hash_message.__str__())
        hash1 = hashlib.sha256(block_dump.encode("ISO-8859-1")).hexdigest()
        # self.current_hash = hash1
        return hash1
    
    def check_and_add_transaction_to_block(self,transaction):
        """
        Appends transaction to block, then checks if block reached capacity.
        """
        self.transactions_list.append(transaction)
        #self.fees += transaction.fees
        for t in self.transactions_list:
            print(t.amount)
        print("transactions list length for this block: " + str(len(self.transactions_list)))
        if self.capacity > len(self.transactions_list):
            print("NOT AT CAPACITY")
            return True
        else:
            print("Block is at capacityyyyyyyyy !!!")
            return False