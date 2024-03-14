import Crypto
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
import json



class Transaction:
    def _init_(self, sender_address, nonce, recipient_address, recipient_port, type, value, message, sender_private_key):
        self.transaction_id = self.hashTransaction() #to hash tou transaction
        self.signature = self.sign_transaction(sender_private_key) #me to private key tou sender
        self.sender_address = sender_address #to public key tou wallet apo to opoio proerxontai ta xrimata
        self.recipient_address = recipient_address #public key 
        self.type = type
        self.nonce=nonce
        self.signature = None
        if (type==0): #coin transaction
            self.amount = value +  value*0.03
        else: #message transaction
            self.amount = len(message)

    def to_dict(self):
        dict = {
            "sender_address": self.sender_address,
            "receiver_address": self.recipient_address,
            "amount" : self.amount,
            "transaction_id" : self.transaction_id,
            "signature" : self.signature
        }
        return dict    

    def sign_transaction(self, private_key): #me private key
        key = RSA.importKey(private_key)
        hash = SHA256.new(self.id.encode('utf-8'))
        signature = PKCS1_v1_5.new(key).sign(hash)
        result = base64.b64encode(signature).decode()
        self.signature = result
        return result

    def verify_signature(self):
        public_key = RSA.import_key(self.sender_address)
        signature = base64.b64decode(self.signature)
        h = SHA256.new(self.transaction_id.encode('utf-8'))
        verifier = PKCS1_v1_5.new(public_key)
        if verifier.verify(h, signature):
            print("Transaction signature is valid")
            verify = True
        else:
            print("Transaction signature is not valid")
            verify = False
        return verify
        

    def hashTransaction(self):
        hash_message = self.to_dict()
        block_dump = json.dumps(hash_message.__str__()) #to kanoume json
        hash = SHA256.new(block_dump.encode("ISO-8859-1")).hexdigest()
        self.current_hash = hash
        return hash
