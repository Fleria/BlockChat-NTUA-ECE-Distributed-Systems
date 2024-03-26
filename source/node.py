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
        self.nonce = 0
        self.wallet = self.generate_wallet()
        self.ring = {self.wallet.address : [0, ip, port, self.BCC,0]} #store information for every node(id, adrdress (ip:port), public key, balance)
        self.current_block = None
        self.blockchain = blockchain.Blockchain()
        self.PoS_select = Lock()
        self.current_validator = None
        self.bootstrap_addr = None
        self.bootstrap_port = None
        self.stake = 0

    def generate_wallet(): #create a wallet for this node, with a public key and a private key. returns the Wallet class
        return wallet.Wallet() #prepei kapos na stelnoume piso to public key
    
    def create_transaction(self, receiver_ad, receiver_port, amount , message): #remember to broadcast it
        trans = transaction.Transaction(self.wallet.address, self.nonce, receiver_ad, receiver_port, amount, message, self.wallet.private_key)
        self.nonce += 1
        trans.nonce = self.nonce #to nonce tis sinallagis einai to nonce tou node
        trans.hashTransaction()
        trans.sign_transaction()
        self.validate_transaction()
        self.add_transaction(trans)
        self.broadcast_transaction(trans)
                    
    def validate_transaction(self, transaction): #use of signature and BCCs balance, change
        if(transaction.verify_signature == True):
            print("Signature verified")
            if (self.wallet.unspent >= transaction.amount):
                print("Balance is enough")
                return True
        else:
            print("transaction couldn't be validated")
            return False
    
    def broadcast_transaction(self,transaction):
        endpoint='/validate_transaction'
        for node in self.ring :
            address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
            response = requests.post(address, transaction)#prepei na broume pos na steiloyme to transaction
            #if response.status_code == 'correct' :#prepei na orisoume to correct. Giati ginetai prota validate kai meta add_to_block.
            if (validate_transaction(transaction) == True):
                return True
            else :
                return False
        if transaction.recipient_address == 0 :
            self.ring[transaction.sender_address][3]+=self.ring[transaction.sender_address][4]
            self.ring[transaction.sender_address][4]=transaction.amount
        else :
            endpoint='/receive_transaction'
            for node in self.ring :
                address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
                response = requests.post(address,transaction)#prepei na broume pos na steiloyme to transaction
                if response.status_code == 'correct' :#prepei na orisoume to correct. Giati ginetai prota validate kai meta add_to_block.
                    return

    def mint_block():
        #ilopoiei to proof of stake kalontas tin gennitria. if called by validator, gemizei ta pedia tou block me tis plirofories
        return
    
    def broadcast_block():
        return

    def validate_block(self):
        self.current_block.myHash()

    def validate_chain():
        return

    def stake(self,amount): 
        self.create_transaction(0,0,amount,None)

    def register_node_to_ring(self, id, ip, port, public_key, balance): #called only by bootstrap
        self.ring[public_key] = [id, ip, port, balance]

    def create_new_block(self):
        self.current_block=block.Block(self.current_block.current_hash)

    def add_transaction(self, transaction): #adds transaction to block, returns false if block is full
        if transaction.sender_address == self.wallet.address or transaction.receipient_address == self.wallet.address :
            self.wallet.transactions.append(transaction)

        self.ring[transaction.sender_address][3] -= transaction.amount
        if transaction.type == 0 :
            self.ring[transaction.receipient_address][3] += transaction.amount

        if self.current_block.check_and_add_transaction(transaction) :
            return True
        else :
            #all the nodes execute proof-of-stake 
            validator = self.select_candidate()
            if self.nonce == validator : 
                self.broadcast_block(self.validate_block(self.current_block))
            self.current_block = block.Block(self.current_block.capacity,self.current_block.index,self.current_block.validator)# to previous hash tha prostethei otan o validating node kanei broadcast to prohgoumeno block
                   
    def select_candidate(self) :
        validator = self.PoS()
        return validator
    
    def Pos() :
        return