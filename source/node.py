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

class node:
    """
    Implementation for each of the 5 nodes of the system.
    """
    def _init_(self,ip,port):
        self.BCC = 100
        self.nonce = 0
        self.id = 0
        self.wallet = self.generate_wallet()
        self.ring = {self.wallet.address : [0, ip, port, self.BCC,0]} #store information for every node(id, adrdress (ip, port), balance, stake)
        self.current_block = None
        self.blockchain = blockchain.Blockchain()
        self.PoS_select = Lock()
        self.current_validator = None
        self.bootstrap_addr = None
        self.bootstrap_port = None
        self.stake = 0
        self.message_fees = 0

    def generate_wallet(): 
        """
        Creates a wallet for this node, with a public and a private key. 
        """
        return wallet.Wallet()
    
    def create_transaction(self, receiver_ad, receiver_port, amount, message):
        """
        Creates a transaction object and initialises it, then broadcasts it.
        """
        trans = transaction.Transaction(self.wallet.address, self.nonce, receiver_ad, receiver_port, amount, message, self.wallet.private_key)
        self.nonce += 1
        trans.nonce = self.nonce #transaction nonce is current node nonce
        trans.hashTransaction()
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
        for node in self.ring :
            address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
            response = requests.post(address, transaction.to_dict())
            if response.status_code == 'correct': #prepei na orisoume to correct
                endpoint='/receive_transaction'
                for node in self.ring :
                    address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
                    response = requests.post(address,transaction)
                    if response.status_code == 'correct':
                        return
            # if (self.validate_transaction(transaction) == True):
            #     self.add_transaction(transaction)
            else :
                print("Transaction couldn't be validated")
    
    def broadcast_block(self,hash):
        endpoint='/valid_block'
        for node in self.ring :
            address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
            response = requests.post(address, transaction.to_dict())
        return

    def validate_block(self): #adam prepei na to ftiaksoume
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

    def register_node_to_ring(self, id, ip, port, public_key, balance): #called only by bootstrap #adam
        self.ring[public_key] = [id, ip, port, balance]

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
        if transaction.sender_address == self.wallet.address or transaction.receipient_address == self.wallet.address :
            self.wallet.transactions.append(transaction)

        self.ring[transaction.sender_address][3] -= (transaction.amount + transaction.fees) #subtract the amount from sender, no matter the transaction type
        
        if transaction.type == 0: #coin 
            self.message_fees += transaction.fees
            self.ring[transaction.receipient_address][3] += transaction.amount

        if transaction.type == 1: #message 
            if transaction.receipient_address == self.wallet.address:
                self.wallet.messages.append(transaction.message)

        if (transaction.type == 2): #stake
            self.ring[transaction.sender_address][3] += self.ring[transaction.sender_address][4]
            self.ring[transaction.sender_address][4] = transaction.amount

        if (self.current_block.check_and_add_transaction_to_block(transaction) == False): #if current block is at capacity, execute proof of stake and create new block
            self.blockchain.add_to_blockchain(self.current_block)
            validator = self.select_validator()
            if self.id == validator : 
                self.broadcast_block(self.validate_block(self.current_block))
            else: 
                for node in self.ring: #adam evala na karatei kathe node ta sinolika fees tou kai na ta prosthetei edo sto wallet tou validator
                    validator[0].wallet.unspent += node.message_fees
            
            self.current_block = block.Block(self.current_block.capacity, self.current_block.index, self.current_block.validator)# to previous hash tha prostethei otan o validating node kanei broadcast to prohgoumeno block
                   
    def select_validator(self):
        """
        Selects a validator for the execution of the Proof-of-Stake algorithm.
        Creates sum of stakes by each node and randomly chooses a treshold.
        Checks if each node's stakes reach the threshold and, if not,
        adds the next node's stakes and tries again.
        """
        total_stakes = sum(amount[4] for amount in self.ring.values())
        threshold = random.uniform(0, total_stakes)
        current = 0
        for node in self.ring:
            current += node[4]
            if current >= threshold:
                validator = node[0]
        return validator
    
    def PoS(self):
        # endpoint='/lottery'
        # for node in self.ring :
        #     address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
        #     response = requests.get(address)
        return
    
    def view_block():
        return

    def balance():
        endpoint='/balance'
        address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
        response = requests.get(address)
        print('Node balance:', response.text)
        return response

    def send_trans():
        return
    
    def mint_block(): #adam
        return 