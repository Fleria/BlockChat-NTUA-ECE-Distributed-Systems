import block
import wallet
import transaction
import blockchain

class node:
    def _init_():
        self.BCC=100
       
        #self.chain
        #self.current_id_count
        #self.NBCs
        #self.wallet
        self.ring = []
        #self.ring[] #here we store information for every node(id, adrdress (ip:port), public key, balance)

    def create_new_block():

    def register_node_to_ring(self, id, ip, port, public_key, balance):
        """Registers a new node in the ring, called only by the bootstrap node"""

        self.ring.append(
            {
                'id': id,
                'ip': ip,
                'port': port,
                'public_key': public_key,
                'balance': balance
            })

    def generate_wallet(): #create a wallet for this node, with a public key and a private key

    def sign_transaction():
    
    def create_transaction(sender, receiver, signature): #remember to broadcast it

    def broadcast_transaction():

    def verify_signature():

    def validate_transaction(): #use of signature and BCCs balance

    def add_transaction_to_block(): #if enough transactions mine

    def mine_block():

    def broadcast_block():

    def validate_block():

    def validate_chain():

    def stake(amount):
