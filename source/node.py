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
from threading import Lock

class node:
    def _init_(self,ip,port):
        self.BCC = 100
        self.nonce=0
        self.wallet = self.generate_wallet()
        self.ring = {self.wallet.address : [0, ip, port, self.BCC]} #store information for every node(id, adrdress (ip:port), public key, balance)
        self.current_block = None
        self.blockchain = blockchain.Blockchain()
        self.PoS_select = Lock()
        self.current_validator = None
        self.bootstrap_addr = None
        self.bootstrap_port=None

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
        endpoint='/validate_transaction'
        for node in self.ring :
            address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
            response = requests.post(address,transaction)#prepei na broume pos na steiloyme to transaction
            if response.status_code == 'correct' :#prepei na orisoume to correct. Giati ginetai prota validate kai meta add_to_block.
                return 
            else :
                return False
        endpoint='/receive_transaction'
        for node in self.ring :
            address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
            response = requests.post(address,transaction)#prepei na broume pos na steiloyme to transaction
            if response.status_code == 'correct' :#prepei na orisoume to correct. Giati ginetai prota validate kai meta add_to_block.
                return 
        
    

    def add_transaction(self, transaction): #adds transaction to block, returns false if block is full
        if transaction.sender_address == self.wallet.address or transaction.receipient_address == self.wallet.address :
            self.wallet.transactions.append(transaction)

        self.ring[transaction.sender_address][3] -= transaction.amount
        if transaction.type == 0 :
            self.ring[transaction.receipient_address][3] += transaction.amount

        if self.current_block.check_and_add_transaction(transaction) :
            return True
        else :
            #execute proof-of-stake
            if self.nonce == 0 : 
                self.select_candidate()
            else :
                #ask bootstrap node for the validator
                endpoint = "request_validator"
                address = 'http://' + self.bootstrap_addr +':'+ self.bootstrap_port + endpoint
                response = requests.get(address) # apo to response pairnoyme ton validator.
                validator = response 
                self.current_block = block.Block(self.current_block.capacity,self.current_block.index,self.current_block.validator)# to previous hash tha prostethei otan o validating node kanei broadcast to prohgoumeno block
                if self.nonce == validator : 
                    self.validate_block()
                    self.broadcast_block()
                

            
    def select_candidate(self) :
        self.PoS_select.acquire()
        self.validator = self.PoS()
        self.PoS_select.release()
        return 
    

    def Pos() :
        return
    #def validate_transaction(): #use of signature and BCCs balance

    #def add_transaction_to_block(): #if enough transactions mine

    #def mine_block():

    def broadcast_block():
        return

    def validate_block(self):
        self.current_block.myHash()

    #def validate_chain():

    #def stake(amount):
