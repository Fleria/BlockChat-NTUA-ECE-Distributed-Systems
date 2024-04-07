import Crypto
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
import json

# def verify_signature2(sender_address,trans_id,signature):
#         """
#         Verifies the signature of the transaction using the sender's public key.
#         Returns True or False accordingly.
#         """
#         public_key = RSA.import_key(sender_address)
#         signature = base64.b64decode(signature)
#         h = trans_id
#         verifier = PKCS1_v1_5.new(public_key)
#         if verifier.verify(h, signature): 
#             print("Transaction signature is valid")
#             verify = True
#         else:
#             print("Transaction signature is not valid")
#             verify = False
#         return verify

class Transaction:
    """
    Implementation for a transaction between two nodes.
    """
    def __init__(self, sender_address, nonce, receiver_address, message, signature=None,id=None):
        self.transaction_id = id #transaction hash
        self.signature = signature
        self.sender_address = sender_address #sender public key
        self.receiver_address = receiver_address # recipient public key 
        self.type = None #type 0: coin, type 1: message, type 2: stake
        self.nonce = nonce
        self.fees = 0
        self.message = message
        self.type = None
        if self.sender_address==0: #stake
            self.type = 2 
            self.amount = int(message)
        else :
            if (self.message.isdigit()): #coin transaction
                self.type = 0
                print("Value is "+str(int(message)))
                self.fees = int(message)*0.03
                self.amount = int(message) + self.fees
            else: #message transaction
                self.type = 1
                self.message = message
                self.amount = len(message)
                self.fees = self.amount
        
    def to_dict(self):
        dict = {
            "sender_address": self.sender_address,
            "receiver_address": self.receiver_address,
            "amount" : self.amount,
            "message" : self.message,
            "type": self.type,
            "transaction_id" : self.transaction_id,
            "signature" : self.signature,
            "nonce" : self.nonce
        }
        return dict  
    def to_dict1(self):
        dict = {
            "sender_address": self.sender_address,
            "receiver_address": self.receiver_address,
            "amount" : self.amount,
            "message" : self.message,
            "type": self.type,
            "nonce" : self.nonce
        }  

    def sign_transaction(self, private_key):
        """
        Signs transaction using sender's private key.
        """
        hash_message = self.to_dict1()
        block_dump = json.dumps(hash_message)
        hash = SHA256.new(block_dump.encode("ISO-8859-1"))
        self.transaction_id=hash.hexdigest()
        hash=SHA256.new(self.transaction_id.encode("ISO-8859-1"))
        key = RSA.importKey(private_key)
        signature = PKCS1_v1_5.new(key).sign(hash)   
        result = base64.b64encode(signature).decode()
        self.signature = result
        print("Transaction has been signed")
        #return result

    def verify_signature(self):
        """
        Verifies the signature of the transaction using the sender's public key.
        Returns True or False accordingly.
        """
        public_key = RSA.import_key(self.sender_address)
        signature = base64.b64decode(self.signature)
        h = SHA256.new(self.transaction_id.encode("ISO-8859-1"))
        verifier = PKCS1_v1_5.new(public_key)
        if verifier.verify(h, signature): 
            verify = True
        else:
            verify = False
        return verify
    
    def hashTransaction(self):
        """
        Creates hash for the transaction object and assigns it to its id.
        """
        hash_message = self.to_dict()
        block_dump = json.dumps(hash_message.__str__()) #to kanoume json
        #print(block_dump)
        hash = SHA256.new(block_dump.encode("ISO-8859-1")).hexdigest()
        self.transaction_id = hash
        return hash
