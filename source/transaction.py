from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import base64


class Transaction:
    def _init_(self, sender_address,type_of_transaction,message, sender_private_key, recipient_address, value):
        #self.sender_address: to public key tou wallet apo to opoio proerxontai ta xrimata
        #self.receiver_address: public key
        #self.transaction_id: to hash tou transaction
        #self.signature: me to private key
        self.sender_address = sender_address 
        self.recipient_address = recipient_address 
        self.amount = value
        self.type = type_of_transaction
        self.signature = None

    def to_dict(self):
    
        dict = {
            "sender_address": self.sender_address,
            "receiver_address": self.receiver_address,
            "amount" : self.amount,
            "transaction_id" : self.transaction_id,
            "transaction_inputs" : self.transaction_inputs,
            "transaction_outputs" : self.transaction_outputs,
            "signature" : self.signature
        }
        return dict    

    def sign_transaction(self,private_key): #me private key
        key = RSA.importKey(private_key)
        hash = SHA256.new(self.id.encode('utf-8'))
        signature = PKCS1_v1_5.new(key).sign(hash)
        result = base64.b64encode(signature).decode()
        self.signature = result
