import block
import node

class Blockchain:
    """
    Implementation for the blockchain.
    """
    def __init__(self):
        self.blocks_of_blockchain = []
        self.length = 0

    def add_to_blockchain(self, block): 
        """
        Adds block to blockchain.
        """
        self.blocks_of_blockchain.append(block)
        self.length += 1

    def to_dict(self):
        blockchain={}
        count=0
        for block in self.blocks_of_blockchain :
            blockchain[str(count)]=block.to_dict1()
            count +=1
        return blockchain