import sys
import requests
from colorama import init, Fore
import json
from argparse import ArgumentParser
from flask import Flask, jsonify, request, render_template
#from flask_cors import CORS
import requests
import json
from argparse import ArgumentParser
import block
import node
import blockchain
import wallet
import transaction
from api_test import rest_api, my_node


my_ip = 'localhost'

init()
COLOR_SUCCESS = Fore.GREEN
COLOR_ERROR = Fore.RED
COLOR_RESET = Fore.RESET

"""
-t <recipient_address> <message>
New transaction: Στείλε στο recipient_address wallet το ποσό amount από BTC coins που θα πάρει
από το wallet sender_address. Θα καλεί συνάρτηση create_transaction στο backend που θα
υλοποιεί την παραπάνω λειτουργία.
-t <recipient_address> <message>
New message: Στείλε στο recipient_address wallet το μήνυμα message χρεώνοντας κατάλληλα το
wallet του αποστολέα. Θα καλεί συνάρτηση create_transaction στο backend που θα
υλοποιεί την παραπάνω λειτουργία.
-stake <amount>
Set the node stake: Δέσμευσε amount ποσό για staking του συγκεκριμένου κόμβου. Καλεί την
stake(amount)όπως ορίστηκε παραπάνω.
-view
View last block: Τύπωσε τα transactions που περιέχονται στο τελευταίο επικυρωμένο block του
BlockChat blockchain καθώς και το id του validator του block αυτού. Καλεί τη συνάρτηση
view_block() στο backend που υλοποιεί την παραπάνω λειτουργία.
-balance
Show balance: Τύπωσε το υπόλοιπο του wallet.
-help
Επεξήγηση των παραπάνω εντολών.
"""


parser = ArgumentParser()
required = parser.add_argument_group()
required.add_argument('-p',type=str,required=True)
args=parser.parse_args()
my_port=args.p


print("This is node " + str(my_port))
print("Enter command or enter <help> to view list of possible commands \n")

help_string = '''
Your options are: \n
t <type> <recipient_address> <message>: create a new transaction from your wallet to <recipient_address>'s wallet. 
If you wish to make a coin transaction, leave <message> empty. \n
stake <amount>: set your stake amount \n
view: print out the transactions of the last validated block of BlockChat and its validator id. \n
balance: print out your wallet balance. \n
'''


while True:
    try:
        action = input()
        words = action.split()
        
        if words[0] == 't':
            id = words[1]
            message = words[2]
            sender = my_port
            endpoint = '/send_transaction'
            address = 'http://' + my_ip + ':' + my_port + endpoint
            stake_flag = 'False'
            # if message.isdigit():
            #     response = requests.post(address, data={'id': id, 'amount': message})
            # else:
            #     response = requests.post(address, data={'id': id, 'message': message})
            response = requests.post(address, data={'id': id, 'message': message, 'sender': sender, 'stake_flag': stake_flag})
            print("\n")
        
        elif words[0] == 'stake':
            stake = words[1]
            stake_flag = 'True'
            endpoint = '/send_transaction'
            address = 'http://' + my_ip + ':' + my_port + endpoint
            response = requests.post(address, {'id': my_port, 'stake': stake, 'stake_flag': stake_flag})
            print("\n")

        elif words[0] == 'view':
            endpoint = '/view_block'
            address = 'http://' + my_ip + ':' + my_port + endpoint
            try:
                response = requests.get(address)
                if response.status_code == 200:
                    response_data = response.json()
                    block_data = response_data['block']
                    block_validator = response_data['validator']
                    block_index = response_data['index']
                    print("The block validator is:")
                    print(block_validator)
                    print("And the list of transaction messages for the block are:")
                    print(block_data)
                    print("\n")
            except:
                print("No valid block yet!")
        
        elif words[0] == 'balance':
            endpoint = '/balance'
            address = 'http://' + my_ip + ':' + my_port + endpoint
            response = requests.get(address)
            data = response.json()
            print('Node balance:', data['balance'])
            print("\n")
        
        elif words[0] == 'help':
            print(help_string)
        
        elif words[0] == 'exit':
            print("Goodbye")
            sys.exit(0)
    
    except KeyboardInterrupt:
        print("Goodbye")
        sys.exit(0)