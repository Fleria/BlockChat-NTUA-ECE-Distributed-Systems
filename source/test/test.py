import requests
import node
import block
import blockchain


endpoint='/balance'
address = 'http://localhost:5000' + endpoint
response = requests.get(address)
if response.status_code==200 :
    print('Balance OK')
data=response.json()
print('Node balance:', data['balance'])

endpoint='/send_transaction'
address = 'http://localhost:5000' + endpoint
data = {'id': 0,'amount':30}
response = requests.post(address,data=data)
if response.status_code==200 :
    print('coin trans')

endpoint='/send_transaction'
address = 'http://localhost:5000' + endpoint
data = {'id': 1,'stake':30}
response = requests.post(address,data=data)
if response.status_code==200 :
    print('stake trans')

endpoint='/send_transaction'
address = 'http://localhost:5000' + endpoint
data = {'id': 2,'message':"h eleftheria goustarei na pinei gala"}
response = requests.post(address,data=data)
if response.status_code==200 :
    print('message trans')

# endpoint='/view_block'
# address = 'http://localhost:5000' + endpoint
# response= requests.get(address)
# if response.status_code==200 :
#     print("View block successful")
#     print(response.content)
# else:
#     print("view block not successful")