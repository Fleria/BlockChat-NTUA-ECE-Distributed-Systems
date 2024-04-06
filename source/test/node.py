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
    def __init__(self,bootstrap_addr,bootstrap_port,ip=None,port=None):
        self.BCC = 1000
        self.nonce = 0
        self.ip=ip
        self.port=port
        self.id = None
        self.wallet = wallet.Wallet()
        # self.ring = {self.wallet.address : [id, ip, port, self.BCC,0]} #store information for every node(id, adrdress (ip, port), balance, stake)
        self.ring={}
        self.current_block = block.Block(1,None)
        self.blockchain = blockchain.Blockchain()
        self.PoS_select = Lock()
        #t 1self.current_validator = None
        self.bootstrap_addr = bootstrap_addr
        self.bootstrap_port = bootstrap_port
        self.my_stake = 10
        self.message_fees = 0
        #self.ring2 = {'my_node_key' : [0, '127.0.0.1', '5000', self.BCC, 0]}

    def register_node_to_ring(self, id, ip, port, public_key, balance): #called only by bootstrap #adam
        self.ring[public_key] = [id, ip, port, balance, self.my_stake]

    # def generate_wallet(): 
    #     """
    #     Creates a wallet for this node, with a public and a private key. 
    #     """
    #     return wallet.Wallet()
    
    def create_transaction(self, receiver_id, amount=None, message=None):
        """
        Creates a transaction object and initialises it, then broadcasts it.
        """
        print("receiver_id == " , receiver_id)
        for key in self.ring :
            print(key, "\n" , self.ring[key],self.ring[key][0])                      # kanoume transaction me node id kai 
            if str(self.ring[key][0]) == receiver_id :   # briskoume to node public key edo
                #print(self.ring[key][0],receiver_id)
                receiver_address=key    
                #print("the key we need is ", receiver_address)
                trans = transaction.Transaction(self.wallet.address, self.nonce, receiver_address, amount, message, self.wallet.private_key)
                self.nonce += 1
                trans.nonce = self.nonce
                trans.sign_transaction(self.wallet.private_key)
                self.broadcast_transaction(trans)
                break
             #
         #transaction nonce is current node nonce
        #self.current_block.check_and_add_transaction_to_block(trans)
        # trans.hashTransaction()
        # trans.sign_transaction(self.wallet.private_key)
        # self.broadcast_transaction(trans)
                    
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
        for node in self.ring.values() :
            if node[0]!=self.id :
                address = 'http://' + node[1] +':'+ node[2] + endpoint
                print("sending transaction to ", address)
                response = requests.post(address, data=transaction.to_dict())
                if response.status_code != 200: 
                    print("transaction couldnt be validated")
                    return False
        endpoint='/receive_transaction'
        for node in self.ring.values() :
            if node[0]!=self.id :
                address = 'http://' + node[1] +':'+ node[2] + endpoint
                response = requests.post(address,data=transaction.to_dict())
                if response.status_code != 200:
                    print("node" , node[0], "couldnt receive transaction")
        print(" successfully broadcast")
        return
                # if (self.validate_transaction(transaction) == True):
                #     self.add_transaction(transaction)
        # address= 'http://localhost:5000'+endpoint
        # response = requests.post(address, data=transaction.to_dict())
        # if response.status_code == 200:
        #     endpoint='/receive_transaction'
        #     address= 'http://localhost:5000'+endpoint
        #     response = requests.post(address,data=transaction.to_dict())
        #     if response.status_code == 200:
        #             print("Transaction successfully broadcast")
        # if (transaction.verify_signature()):
        #      print("Transaction signature is verified")
        #      self.add_transaction(transaction)
        # else :
        #     print("Transaction couldn't be validated")

    def broadcast_block(self, hash):
        endpoint='/receive_valid_block'
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
        # if transaction.sender_address == self.wallet.address or transaction.receiver_address == self.wallet.address :
        #     self.wallet.transactions.append(transaction)
        self.wallet.transactions.append(transaction)
        print("old sender amount" ,self.ring[transaction.sender_address][3] )
        self.ring[transaction.sender_address][3] -= (transaction.amount) #subtract the amount from sender, no matter the transaction type
        print("new sender amount" ,self.ring[transaction.sender_address][3] )
        if transaction.type == 0: #coin 
            self.current_block.fees += transaction.fees
            self.ring[transaction.receiver_address][3] += transaction.amount
            print("coin transaction added") #testing

        if transaction.type == 1: #message 
            if transaction.receiver_address == self.wallet.address:
                self.wallet.messages.append(transaction.message)
                self.current_block.fees += transaction.fees
                print("message transaction added") #testing

        if (transaction.type == 2): #stake
            self.ring[transaction.sender_address][3] += self.ring[transaction.sender_address][4]
            self.ring[transaction.sender_address][4] = transaction.amount
            print("stake transaction added") #testing

        # if (self.current_block.check_and_add_transaction_to_block(transaction) == True): #testing
        #     return
        
        if (self.current_block.check_and_add_transaction_to_block(transaction) == False): #if current block is at capacity, execute proof of stake and create new block
            sorted_ring = {k: v for k, v in sorted(self.ring.items(), key=lambda item: int(item[1][0]))}
            for address, values in sorted_ring.items():
                print(f"ID: {values[0]}, IP: {values[1]}, Port: {values[2]}, BCC: {values[3]}, SomeValue: {values[4]}")
            self.blockchain.add_to_blockchain(self.current_block)
            print("Current length of blockchain is: " + str(len(self.blockchain.blocks_of_blockchain))) #testing
            validator = self.select_validator()
            print("Validator is " + str(validator))
            self.current_block.validator = validator
            if self.id == validator : 
                self.broadcast_block(self.current_block.current_hash) 
                print("Capacity: " + str(self.current_block.capacity))
                self.broadcast_block(self.current_block.capacity) #testing
            else: 
                for address, node_info in sorted_ring.items():
                    if node_info[0] == validator:
                        target_address = address
                sorted_ring[target_address][3] += self.current_block.fees
            
            #self.current_block.index+=1 prepei na to ftiaksoume
            self.current_block = block.Block(self.current_block.index, self.current_block.validator)# to previous hash tha prostethei otan o validating node kanei broadcast to prohgoumeno block
            self.current_block.index+=1

    def select_validator(self):
        """
        Selects a validator for the execution of the Proof-of-Stake algorithm.
        Creates sum of stakes by each node and randomly chooses a treshold.
        Checks if each node's stakes reach the threshold and, if not,
        adds the next node's stakes and tries again.
        """
        number = self.current_block.myHash() #kanonika thelei previous hash, na to ftiaksoume sto telos
        random.seed(number) 
        total_stakes = sum(amount[4] for amount in self.ring.values())
        threshold = random.uniform(0, total_stakes)
        print("Threshold is "+str(threshold))
        current = 0
        for node in self.ring.values():
            print("my id is "+str(node[0]))
            node_index = int(node[4])
            current += node_index
            print(current)
            if current >= threshold:
                validator = node[0]
                print("VALIDATOR IS NODE "+str(validator))
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