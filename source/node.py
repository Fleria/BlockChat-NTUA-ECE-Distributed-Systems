import block
import wallet
import transaction
import blockchain
import Crypto
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
import requests

class node:
    def _init_(self,ip,port):
        self.BCC = 100
        self.nonce=0
        self.wallet = self.generate_wallet()
        self.ring = {self.wallet.address : [0, ip, port, self.BCC]} #store information for every node(id, adrdress (ip:port), public key, balance)
        self.current_block = None

    def register_node_to_ring(self, id, ip, port, public_key, balance): #called only by bootstrap
        self.ring[public_key] = [id, ip, port, balance]

    def generate_wallet(): #create a wallet for this node, with a public key and a private key. returns the Wallet class
        return wallet.Wallet() #prepei kapos na stelnoume piso to public key

    def create_new_block(self):
        self.current_block=block.Block(self.current_block.current_hash)
    
    def create_transaction(self, receiver_ad, receiver_port, amount , message): #remember to broadcast it
        trans = transaction.Transaction(self.wallet.address,self.nonce,receiver_ad,receiver_port,amount,message )
        self.nonce += 1
        trans.signature = self.sign_transaction()
        self.broadcast_transaction(trans)

    def broadcast_transaction(self,transaction):
        endpoint='/receive_transaction'
        for node in self.ring :
            address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
            response = requests.post(address,transaction)#prepei na broume pos na steiloyme to transaction
            if response.status_code == 'correct' :#prepei na orisoume to correct. Giati ginetai prota validate kai meta add_to_block.
                return 

    #def validate_transaction(): #use of signature and BCCs balance

    #def add_transaction_to_block(): #if enough transactions mine

    #def mine_block():

    #def broadcast_block():

    #def validate_block():

    #def validate_chain():

    #def stake(amount):
