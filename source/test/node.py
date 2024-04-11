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
        # self.ring = {self.wallet.address : [id, ip, port, self.BCC, stake]} #store information for every node(id, adrdress (ip, port), balance, stake)
        self.ring={}
        self.current_block = block.Block(0)
        self.blockchain = blockchain.Blockchain()
        self.bootstrap_addr = bootstrap_addr
        self.bootstrap_port = bootstrap_port
        self.my_stake = 10
        self.message_fees = 0
        self.current_validator = 0
        self.blocklock= Lock()

    def register_node_to_ring(self, id, ip, port, public_key, balance): #called only by bootstrap 
        self.ring[public_key] = [id, ip, port, balance, self.my_stake]

    # def generate_wallet(): 
    #     """
    #     Creates a wallet for this node, with a public and a private key. 
    #     """
    #     return wallet.Wallet()
    
    def create_transaction(self, sender_port, receiver_id, message, stake):
        """
        Creates a transaction object and initialises it, then broadcasts it.
        """
        #print("receiver_id == " , receiver_id)
        if(stake==True):
            #print("Creating transaction with stake!")
            for key in self.ring :
                if str(self.ring[key][2]) == receiver_id :
                    receiver_address=key
                    for public_key, node_info in self.ring.items():
                        _, _, port, _, _ = node_info
                        if port == sender_port:
                            sender_public_key = public_key
                            #print("stake transaction sender ",sender_public_key)
                            break
                    trans = transaction.Transaction(sender_public_key, self.nonce, receiver_address, message, stake=True)
                    trans.sign_transaction(self.wallet.private_key)
                    return self.broadcast_transaction(trans)
                    break    

            #print("This is a stake transaction")

        else:
            for key in self.ring : #every node does this
                #print(key, "\n" , self.ring[key],self.ring[key][0]) # transaction made node id
                if str(self.ring[key][0]) == receiver_id :  # match to node public key
                    #print(self.ring[key][0],receiver_id)
                    receiver_address=key    
                    #print("the key we need is ", receiver_address)
                    for public_key, node_info in self.ring.items():
                        _, _, port, _, _ = node_info  # Extract the port number from the node information
                        if port == sender_port:
                            sender_public_key = public_key
                            # Found the node with the matching port number
                            #print("Public key:", public_key)
                            break
                    trans = transaction.Transaction(sender_public_key, self.nonce, receiver_address, message)
                    self.nonce += 1
                    trans.nonce = self.nonce
                    trans.sign_transaction(self.wallet.private_key)
                    return self.broadcast_transaction(trans)
                    break
                    
    def validate_transaction(self, transaction): 
        """
        Checks to verify the signature of the transaction and the balance of the wallet. 
        If verified, validates the transaction.
        """
        if (transaction.verify_signature() == True):
            print("Signature verified")
            if (self.ring[transaction.sender_address][3] >= transaction.amount):
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
        target_address = transaction.sender_address
        for public_key, node_info in self.ring.items():
            if public_key == target_address:
                target_port = node_info[2]
        endpoint='/validate_transaction'
        for node in self.ring.values() :
            #if node[0]!=self.id :
                address = 'http://' + node[1] +':'+ node[2] + endpoint
                print("Now sending transaction to ", address)
                response = requests.post(address, data=transaction.to_dict())
                if response.status_code != 200: 
                    print("Transaction couldn't be validated")
                    return False
                else:
                    print("Transaction validated through broadcast")
        endpoint='/receive_transaction'
        responses=[]
        for node in self.ring.values() : #ola ta nodes
            #if node[0]!=self.id :
                address = 'http://' + node[1] +':'+ node[2] + endpoint
                response = requests.post(address, data=transaction.to_dict())
                responses.append(response.status_code)
        if responses[0] >=400 :
            print("Mode couldn't receive transaction ")
            return False
        if responses[0] == 205: #block is full
            validators=[]
            endpoint='/select_validator'
            for node in self.ring.values() :
                address = 'http://' + node[1] +':'+ node[2] + endpoint
                response = requests.get(address)
                data=response.json()
                validators.append(data)
            for id in validators :
                print(" id :", id,"\n")
            validator=validators[0]['validator_id']
            for node in self.ring.values() :
                if node[0]==validator:
                    endpoint='/validate_block'
                    address = 'http://' + node[1] +':'+ node[2] + endpoint
                    response=requests.get(address)
                    hash=response.json()['hash']
                    for key,info in self.ring.items() :
                        if info[0]==validator:
                            self.ring[key][3]+=self.current_block.fees
                    #print('Calculated block hash as ' , hash)
                    for node in self.ring.values():
                        endpoint='/receive_block'
                        address = 'http://' + node[1] +':'+ node[2] + endpoint
                        response=requests.post(address,{'hash':hash,'validator':validator})
                        if response.status_code==200 :
                            print("Block successfuly validated")
        print(" successfully broadcasted the transaction from node " + str(target_port) + " for all nodes"+"\n")
        return True

    def broadcast_block(self, hash,  validator_id):
        """
        Validator broadcasts block to every node in the ring.
        """
        endpoint = '/broadcast_block'
        for node in self.ring.values() :
                address = 'http://' + node[1] +':'+ node[2] + endpoint
                response = requests.post(address,{'hash':hash, 'validator':validator_id})
        if response.status_code != 200:
             print("Block couldn't be validated")
        return
    
    def validate_block(self,hash,validator_id):
        """
        Enters the correct information for the full block and validates it.
        """
        self.blockchain.blocks_of_blockchain[-1].current_hash=hash
        self.blockchain.blocks_of_blockchain[-1].validator=validator_id
        self.current_block.previous_hash=hash

    def stake(self,sender,id,amount): 
        #print("stake amount is ", amount)
        self.create_transaction(sender,id,amount,True)
        return

    def calculate_block_hash(self) :
        return self.current_block.myHash()

    def add_transaction(self, transaction): #tevery node calls
        """
        Adds the transaction to the block. 
        If the current node is either the sender or the receiver, 
        the transaction is appended to the node's list of transactions.
        Balances the wallets accordingly.
        Checks if current block is full after adding the transaction.
        """
        target_address = transaction.sender_address
        for public_key, node_info in self.ring.items():
            if public_key == target_address:
                target_port = node_info[2]
        
        if(transaction.stake == 'True'):
            self.my_stake = transaction.amount
            self.ring[transaction.receiver_address][3] += self.ring[transaction.receiver_address][4] #add back old stake amount
            self.ring[transaction.receiver_address][3] -= (transaction.amount)
            self.ring[transaction.receiver_address][4] = transaction.amount
            print("New stake is ", self.ring[transaction.receiver_address][4])
        
        else:
            if transaction.sender_address == self.wallet.address or transaction.receiver_address == self.wallet.address :
                # print("I am either the server or the receiver of the trasnaction")
                # sender_wallet = sender_node_info[4]
                # sender_wallet.transactions.append(transaction)
                # sender_wallet.balance -= transaction.amount

                # receiver_wallet = receiver_node_info[4]
                # receiver_wallet.transactions.append(transaction)
                # receiver_wallet.balance += transaction.amount
                #transaction.sender_address.wallet.transactions.append(transaction)
                #transaction.receiver_address.wallet.transactions.append(transaction)
                self.wallet.transactions.append(transaction)

            print("Sender is", target_port)
            print("Old sender amount" ,self.ring[transaction.sender_address][3] )
            self.ring[transaction.sender_address][3] -= (transaction.amount) #subtract the amount from sender, no matter the transaction type
            print("New sender amount" ,self.ring[transaction.sender_address][3] )
            
            if transaction.type == 0: #coin 
                self.current_block.fees += transaction.fees
                print("Old receiver amount ", str(self.ring[transaction.receiver_address][3]))
                self.ring[transaction.receiver_address][3] += (transaction.amount - transaction.fees)
                print("New receiver amount ", str(self.ring[transaction.receiver_address][3]))
                print("Coin transaction added") #testing

            if transaction.type == 1: #message
                if transaction.receiver_address == self.wallet.address:
                    self.wallet.messages.append(transaction.message)
                self.current_block.fees += transaction.fees #maybe need to be stored in ring?
                print("Message transaction added, transaction fees are ", transaction.fees) #testing

            if (transaction.type == 2): #stake
                self.ring[transaction.sender_address][3] += self.ring[transaction.sender_address][4]
                self.ring[transaction.sender_address][4] = transaction.amount
                print("Stake transaction added") #testing
            
            if self.current_block.check_and_add_transaction_to_block(transaction) == False :
                return 205 #if current block is at capacity, execute proof of stake and create new block
                # print("locking the the blocklock")
                # self.blocklock.acquire()
                # sorted_ring = {k: v for k, v in sorted(self.ring.items(), key=lambda item: int(item[1][0]))}
                # for address, values in sorted_ring.items():
                #     print(f"ID: {values[0]}, IP: {values[1]}, Port: {values[2]}, BCC: {values[3]}, Stake: {values[4]}")
                # self.blockchain.add_to_blockchain(self.current_block)
                # index = self.current_block.index
                # # print("Current length of blockchain is: " + str(len(self.blockchain.blocks_of_blockchain))) #testing
                # validator = self.select_validator()
                # print("Validator is " + str(validator))
                # self.current_block.validator = validator
                # """
                # This continues the mint_block function.
                # """
                # #if(self.validate_block(self.current_block.previous_hash, validator)):
                # if str(self.id) == str(validator) :
                #     print(" im node ",self.id, " the validator")
                #     hash = self.calculate_block_hash()
                #     print( "block has is ", hash)
                #     self.broadcast_block(hash, validator)

                #     # for key, value in self.ring.items():
                #     #     if value[0] == self.id:
                #     #         validator_key = key
                    
                #     # self.ring[validator_key][3] += self.current_block.fees 
                # # else: 
                # #     for address, node_info in sorted_ring.items():
                # #         if node_info[0] == validator:
                # #             target_address = address
                # #     sorted_ring[target_address][3] += self.current_block.fees
                # for key, value in self.ring.items():
                #         if value[0] == validator:
                #             validator_key = key
                    
                # self.ring[validator_key][3] += self.current_block.fees
                # self.current_block = block.Block(index,validator)

                # # self.current_block.current_hash = self.current_block.myHash
                # self.current_block.index+=1
                # self.blocklock.release()

    def select_validator(self):
        """
        Selects a validator for the execution of the Proof-of-Stake algorithm.
        Creates sum of stakes by each node and randomly chooses a treshold.
        Checks if each node's stakes reach the threshold and, if not,
        adds the next node's stakes and tries again.
        This is the mint_block function.
        """
        sorted_ring = {k: v for k, v in sorted(self.ring.items(), key=lambda item: int(item[1][0]))}
        print("The seed for the random generator is ", self.current_block.previous_hash)
        random.seed(self.current_block.previous_hash)
        total_stakes = sum(amount[4] for amount in sorted_ring.values())
        threshold = random.uniform(0, total_stakes)
        print("Threshold is "+str(threshold))
        current = 0
        for node in sorted_ring.values():
            #print("My id is "+str(node[0]))
            node_index = int(node[4])
            current += node_index
            print(current)
            if current >= threshold:
                validator = node[0]
                #print("VALIDATOR IS NODE "+str(validator))
                break
        self.current_validator = validator
        return validator
      
    def view_block(self, block):
        return block.to_dict()

    def balance(self):
        return self.ring[self.wallet.address][3]