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
import random

class Node:
    """
    Implementation for each of the 5 nodes of the system.
    """
    def __init__(self,ip=None,port=None):
        self.BCC = 1000
        self.nonce = 0
        self.id = 0
        self.wallet = wallet.Wallet()
        self.ring = {self.wallet.address : [0, ip, port, self.BCC,0]} #store information for every node(id, adrdress (ip, port), balance, stake)
        self.current_block = block.Block(1,None)
        self.blockchain = blockchain.Blockchain()
        self.PoS_select = Lock()
        self.current_validator = None
        self.bootstrap_addr = None
        self.bootstrap_port = None
        self.stake = 0
        self.message_fees = 0
        self.ring2 = {'my_node_key' : [0, '127.0.0.1', '5000', self.BCC, 0]}

    def register_node_to_ring(self, id, ip, port, public_key, balance): #called only by bootstrap #adam

        self.ring[public_key] = [id, ip, port, balance]

    # def generate_wallet(): 
    #     """
    #     Creates a wallet for this node, with a public and a private key. 
    #     """
    #     return wallet.Wallet()
    
    def create_transaction(self, receiver_address, amount, message):
        """
        Creates a transaction object and initialises it, then broadcasts it.
        """
        #print(self.id)
        trans = transaction.Transaction(self.wallet.address, self.nonce, receiver_address, amount, message, self.wallet.private_key)
        self.nonce += 1
        trans.nonce = self.nonce #transaction nonce is current node nonce
        self.current_block.check_and_add_transaction_to_block(trans)
        # trans.hashTransaction()
        trans.sign_transaction(self.wallet.private_key)
        self.broadcast_transaction(trans)
                    
    def validate_transaction(self, transaction): 
        """
        Checks to verify the signature of the transaction and the balance of the wallet. 
        If verified, validates the transaction.
        """
        if (transaction.verify_signature() == True):
            print("Signature verified")
            if (self.wallet.unspent >= transaction.amount):
                print("Balance is enough")
                return True
        else:
            print("Transaction couldn't be validated")
            return False
    
    def broadcast_transaction(self,transaction):
        """
        Broadcasts the transaction to every registered node in the ring.
        If the transaction is validated by the node, it gets added to the transaction list.
        """
        endpoint='/validate_transaction'
        # for node in self.ring :
        #     # address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
        #     address= 'http://localhost:5000'+endpoint
        #     response = requests.post(address, data=transaction.to_dict())
        #     if response.status_code == 200: #prepei na orisoume to correct
        #         endpoint='/receive_transaction'
        #         address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
        #         response = requests.post(address,data=transaction.to_dict())
        #         if response.status_code == 200:
        #                 print(" successfully broadcast")
        #     # if (self.validate_transaction(transaction) == True):
        #     #     self.add_transaction(transaction)
        #     else :
        #         print("Transaction couldn't be validated")
        address= 'http://localhost:5000'+endpoint
        response = requests.post(address, data=transaction.to_dict())
        if response.status_code == 200:
            endpoint='/receive_transaction'
            address= 'http://localhost:5000'+endpoint
            response = requests.post(address,data=transaction.to_dict())
            if response.status_code == 200:
                    print(" successfully broadcast")
        if (transaction.verify_signature()):
             print("transaction added successfully to current block " + str(self.current_block)+ ", id is" + str(transaction.transaction_id)) #testing
             self.add_transaction(transaction)
        else :
            print("Transaction couldn't be validated")

    def broadcast_block(self, hash):
        print("lalala")
        endpoint='/receive_valid_block'
        print("lololo")
        print(self.current_block.current_hash)
        #for node in self.ring2 :
            #address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
        address= 'http://localhost:5000'+endpoint
        response = requests.post(address,data={'hash':hash})
        return

    def validate_block(self):
        """
        Αυτή η συνάρτηση καλείται από τους nodes κατά τη λήψη ενός νέου block (εκτός του genesis block).
        Επαληθεύεται ότι (a) ο validator είναι πράγματι ο σωστός (αυτός που υπέδειξε η κλήση της
        ψευδοτυχαίας γεννήτριας) και ότι (b) το πεδίο previous_hash ισούται πράγματι με το hash του
        προηγούμενου block.
        """
        return self.current_block.myHash()

    def validate_chain():
        return

    def stake(self,amount): 
        self.create_transaction(0,0,amount,None)

    # def create_new_block(self):
    #     self.current_block=block.Block(self.current_block.current_hash)

    def add_transaction(self, transaction): 
        """
        Adds the transaction to the block. 
        If the current node is either the sender or the receiver, 
        the transaction is appended to the node's list of transactions.
        Balances the wallets accordingly.
        Checks if current block is full after adding the transaction.
        """
        if transaction.sender_address == self.wallet.address or transaction.reciever_address == self.wallet.address :
            self.wallet.transactions.append(transaction)

        self.ring[transaction.sender_address][3] -= (transaction.amount) #subtract the amount from sender, no matter the transaction type
        
        if transaction.type == 0: #coin 
            self.current_block.fees += transaction.fees
            self.ring[transaction.reciever_address][3] += transaction.amount
            print("coin transaction added") #testing

        if transaction.type == 1: #message 
            if transaction.reciever_address == self.wallet.address:
                self.wallet.messages.append(transaction.message)
                self.current_block.fees += transaction.fees
                print("message transaction added") #testing

        if (transaction.type == 2): #stake
            self.ring[transaction.sender_address][3] += self.ring[transaction.sender_address][4]
            self.ring[transaction.sender_address][4] = transaction.amount
            print("stake transaction added") #testing

        if (self.current_block.check_and_add_transaction_to_block(transaction) == True): #testing
            return
        
        if (self.current_block.check_and_add_transaction_to_block(transaction) == False): #if current block is at capacity, execute proof of stake and create new block
            self.blockchain.add_to_blockchain(self.current_block)
            validator = self.select_validator()
            if self.id == validator : 
                print("I am the validator")
                #self.broadcast_block(self.current_block.current_hash) 
                self.broadcast_block(self.current_block.capacity) #testing here now
            else: 
                validator[0].wallet.unspent += self.current_block.fees
            
            self.current_block = block.Block(self.current_block.index, self.current_block.validator)# to previous hash tha prostethei otan o validating node kanei broadcast to prohgoumeno block
                   
    def select_validator(self):
        """
        Selects a validator for the execution of the Proof-of-Stake algorithm.
        Creates sum of stakes by each node and randomly chooses a treshold.
        Checks if each node's stakes reach the threshold and, if not,
        adds the next node's stakes and tries again.
        """
        total_stakes = sum(amount[4] for amount in self.ring2.values())
        threshold = random.uniform(0, total_stakes)
        current = 0
        for node in self.ring2.values():
            node_index = int(node[4])
            current += node_index
            if current >= threshold:
                validator = node[0]
        return validator
    
    def PoS(self):
        # endpoint='/lottery'
        # for node in self.ring :
        #     address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
        #     response = requests.get(address)
        return
      
    def view_block(self, block):
        return block.to_dict()

    def balance(self):
        return self.BCC
    
    def send_trans():
        return
    
    def mint_block(): #adam
        return 