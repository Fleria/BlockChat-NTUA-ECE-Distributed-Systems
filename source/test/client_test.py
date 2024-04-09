import sys
import requests
from colorama import init, Fore
import json
from flask import Flask, jsonify, request, render_template
from argparse import ArgumentParser
import os

my_ip = 'localhost'

init()
COLOR_SUCCESS = Fore.GREEN
COLOR_ERROR = Fore.RED
COLOR_RESET = Fore.RESET

parser = ArgumentParser()
required = parser.add_argument_group()
required.add_argument('-p', type=str, required=True)
args = parser.parse_args()
my_port = args.p

print("This is node " + str(my_port))

help_string = '''
Your options are: \n
id<recipient_id> <amount>: create a new transaction from your wallet to <recipient_id>'s wallet with the given amount. \n
stake <amount>: set your stake amount \n
view: print out the transactions of the last validated block of BlockChat and its validator id. \n
balance: print out your wallet balance. \n
'''

def read_transactions_from_file(file_path):
        with open(file_path, 'r') as file:
            transactions = file.readlines()
        return [transaction.strip() for transaction in transactions]
file_path = os.path.join('5nodes', 'trans0.txt')
transactions = read_transactions_from_file(file_path)

for action in transactions:
    words = action.split(maxsplit=1)
    
    if not words:
        break
    
    if words[0].startswith('id'):
        recipient_id = words[0][2:]
        amount = words[1].strip()
        sender = my_port
        endpoint = '/send_transaction'
        address = 'http://' + my_ip + ':' + my_port + endpoint
        stake_flag = 'False'
        response = requests.post(address, data={'id': recipient_id, 'message': amount, 'sender': sender, 'stake_flag': stake_flag})
    
    elif words[0] == 'stake':
        stake = words[1].strip()
        stake_flag = 'True'
        endpoint = '/send_transaction'
        address = 'http://' + my_ip + ':' + my_port + endpoint
        response = requests.post(address, {'id': my_port, 'stake': stake, 'stake_flag': stake_flag})
    
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
        except:
            print("No valid block yet!")
    
    elif words[0] == 'balance':
        endpoint = '/balance'
        address = 'http://' + my_ip + ':' + my_port + endpoint
        response = requests.get(address)
        data = response.json()
        print('Node balance:', data['balance'])

transaction_file.close()