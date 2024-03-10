import block
import wallet
import transaction
import blockchain
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import base64
import requests

class node:
    def _init_(self,ip,port):
        self.BCC=100
       
        #self.chain
        #self.current_id_count
        #self.NBCs
        self.nonce=0
        self.wallet = self.generate_wallet()
        self.ring = {self.wallet.address : [0,ip,port,self.BCC]}
        self.current_block = None
        #self.ring[] #here we store information for every node(id, adrdress (ip:port), public key, balance)

    def create_new_block():
        self.current_block=block.Block(self.current_block.current_hash)
    def register_node_to_ring(self, id, ip, port, public_key, balance):
        """Registers a new node in the ring, called only by the bootstrap node"""
        self.ring[public_key] = [id,ip,port,balance]

    def generate_wallet(): #create a wallet for this node, with a public key and a private key
        wallet.Wallet() #prepei kapos na stelnoume piso to publick key

    def sign_transaction(self):
        key = RSA.importKey(self.wallet.private_key)
        hash = SHA256.new(self.id.encode('utf-8'))
        signature = PKCS1_v1_5.new(key).sign(hash)
        result = base64.b64encode(signature).decode()
        return result
    
    def create_transaction(self, receiver_ad, receiver_port, amount , message): #remember to broadcast it
        trans = transaction.Transaction(self.wallet.address,self.nonce,receiver_ad,receiver_port,amount,message )
        self.nonce += 1
        trans.signature = self.sign_transaction()
        self.broadcast_transaction(trans)

    def broadcast_transaction(self,transaction):
        endpoint='/receive_transaction'
        for node in self.ring :
            address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
            response = requests.post(address,transaction)#prepei na broume pos na steiloyme to transaction)
            if response.status_code = correct :#prepei na orisoume to correct. Giati ginetai prota validate kai meta add_to_block.
                return 


    def verify_signature():

    def validate_transaction(): #use of signature and BCCs balance

    def add_transaction_to_block(): #if enough transactions mine

    def mine_block():

    def broadcast_block():

    def validate_block():

    def validate_chain():

    def stake(amount):
