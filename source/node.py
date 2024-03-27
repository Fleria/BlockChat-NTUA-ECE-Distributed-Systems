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
            #if response.status_code == 'correct': #prepei na orisoume to correct
            if (self.validate_transaction(transaction) == True):
                self.add_transaction(transaction)
            else :
                print("Transaction couldn't be validated")
        """
        adam theoro auto to kommati prepei na to valoume sto add_transaction alla to afino kai edo
        """
        if transaction.type == 2 : #stake transaction
            self.ring[transaction.sender_address][3] += self.ring[transaction.sender_address][4]
            self.ring[transaction.sender_address][4] = transaction.amount
        else :
            endpoint='/receive_transaction'
            for node in self.ring :
                address = 'http://' + str(node[1]) +':'+ str(node[2]) + endpoint
                response = requests.post(address,transaction)
                if response.status_code == 'correct':
                    return

    def mint_block():
        #ilopoiei to proof of stake kalontas tin gennitria. if called by validator, gemizei ta pedia tou block me tis plirofories
        return
    
    def broadcast_block():
        return

    def validate_block(self):
        self.current_block.current_hash = self.current_block.myHash()

    def validate_chain():
        return

    def stake(self,amount): 
        self.create_transaction(0,0,amount,None)

    def register_node_to_ring(self, id, ip, port, public_key, balance): #called only by bootstrap
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

        self.ring[transaction.sender_address][3] -= transaction.amount #subtract the amount from sender, no matter the transaction type
        
        if (transaction.type == 0 or transaction.type == 1): #coin or message
            self.ring[transaction.receipient_address][3] += transaction.amount

        if (transaction.type == 2): #stake
            self.ring[transaction.sender_address][4] = transaction.amount

        if (self.current_block.check_and_add_transaction_to_block(transaction) == True): #if current block isn't at capacity
            return True
        
        else: #if current block is at capacity, execute proof of stake and create new block
            validator = self.select_candidate()
            if self.id == validator : 
                self.broadcast_block(self.validate_block(self.current_block))
            self.current_block = block.Block(self.current_block.capacity, self.current_block.index, self.current_block.validator)# to previous hash tha prostethei otan o validating node kanei broadcast to prohgoumeno block
                   
    def select_candidate(self) :
        validator = self.PoS()
        return validator
    
    def Pos() :
        return