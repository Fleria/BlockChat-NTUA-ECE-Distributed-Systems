import sys
import node

"""
t <recipient_address> <message>
New transaction: Στείλε στο recipient_address wallet το ποσό amount από BTC coins που θα πάρει
από το wallet sender_address. Θα καλεί συνάρτηση create_transaction στο backend που θα
υλοποιεί την παραπάνω λειτουργία.
t <recipient_address> <message>
New message: Στείλε στο recipient_address wallet το μήνυμα message χρεώνοντας κατάλληλα το
wallet του αποστολέα. Θα καλεί συνάρτηση create_transaction στο backend που θα
υλοποιεί την παραπάνω λειτουργία.
stake <amount>
Set the node stake: Δέσμευσε amount ποσό για staking του συγκεκριμένου κόμβου. Καλεί την
stake(amount)όπως ορίστηκε παραπάνω.
view
View last block: Τύπωσε τα transactions που περιέχονται στο τελευταίο επικυρωμένο block του
BlockChat blockchain καθώς και το id του validator του block αυτού. Καλεί τη συνάρτηση
view_block() στο backend που υλοποιεί την παραπάνω λειτουργία.
balance
Show balance: Τύπωσε το υπόλοιπο του wallet.
help
Επεξήγηση των παραπάνω εντολών.
"""

print("Enter command or enter <help> to view list of possible commands \n")

help_string = '''
Your options are: \n
t <recipient_address> <message>: create a new transaction from your wallet to <recipient_address>'s wallet. 
If you wish to make a coin transaction, leave <message> empty. \n
stake <amount>: set your stake amount \n
view: print out the transactions of the last validated block of BlockChat and its validator id. \n
balance: print out your wallet balance. \n
'''

while (1):
    action = input()
    words = action.split()
    
    if (words[0] == 't'):
        id = words[1]
        message = words[2]
        node.send_trans(id, message)
    
    if (words[0] == 'stake'):
        stake = words[1]
        node.send_trans(id, '')
        #call stake_amount

    if (words[0] == 'view'):
        node.view()
        #call view_block
    
    if (words[0] == 'balance'):
        node.balance()
    
    if (words[0] == 'help'):
        print(help_string)

    if (words[0] == 'exit'):
        print("Goodbye")
        sys.exit(0)