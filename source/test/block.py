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
    
    def to_dict1(self):
        transaction_li= map(lambda x : x.to_dict(),self.transactions_list)
        dictio = {
            "index":self.index,
            "validator" : self.validator,
            "transactions_list": dict(list(enumerate(transaction_li))),
            "previous_hash": self.previous_hash,
            "current_hash":self.current_hash
        }
        return dictio

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
        block_dump = json.dumps(hash_message.__str__())
        hash1 = hashlib.sha256(block_dump.encode("ISO-8859-1")).hexdigest()
        return hash1
    
    def check_and_add_transaction_to_block(self,transaction):
        """
        Appends transaction to block, then checks if block reached capacity.
        """
        self.transactions_list.append(transaction)
        #for t in self.transactions_list:
        #    print(t.amount)
        if self.capacity > len(self.transactions_list):
            print("Block is not at capacity yet")
            return True
        else:
            print("Block is at capacity !")
            return False