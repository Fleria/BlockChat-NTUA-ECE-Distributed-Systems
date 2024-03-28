import sys
import node

"""
1: t <recipient_address> <message>
2: stake <amount>
3: view
4: balance
5: help
"""

print("Enter command \n")

help_string = '1: t <recipient_address> <message>, 2: stake <amount>, 3: view, 4: balance, 5: help, 6: exit'

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

    if (words[0] == 'view'):
        node.view()
    
    if (words[0] == 'balance'):
        node.balance()
    
    if (words[0] == 'help'):
        print(help_string)

    if (words[0] == 'exit'):
        print("Goodbye")
        sys.exit(0)