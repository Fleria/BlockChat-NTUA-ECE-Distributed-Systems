import block

class Blockchain:
    def __init__(self):
        self.blocks_of_blockchain = []

    def add_to_blockchain(self, block): #afou exei ginei elegxos, mporoume na tin valoume kai allou auti ti sinartisi
        self.blocks_of_blockchain.append(block)