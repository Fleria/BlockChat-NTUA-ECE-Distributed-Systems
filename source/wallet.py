from Crypto.PublicKey import RSA

class Wallet:
    """
    Implementation for the wallet of each node.
    """
    def __init__(self):
        key = RSA.generate(2048)
        self.private_key = key.exportKey().decode("ISO-8859-1")
        self.public_key = key.publickey().exportKey().decode("ISO-8859-1")
        self.address = self.public_key
        self.unspent = 1000 #change later
        self.transactions = []