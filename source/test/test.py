import requests


endpoint='/balance'
address = 'http://localhost:5000' + endpoint
response = requests.get(address)
if response.status_code==200 :
    print('ok')
data=response.json()
print('Node balance:', data['balance'])

endpoint='/send_transaction'
address = 'http://localhost:5000' + endpoint
data = {'id': 540540540,'amount':30}
response = requests.post(address,data=data)
if response.status_code==200 :
    print('coin trans')

endpoint='/send_transaction'
address = 'http://localhost:5000' + endpoint
data = {'id': 540540540,'stake':30}
response = requests.post(address,data=data)
if response.status_code==200 :
    print('stake trans')

endpoint='/send_transaction'
address = 'http://localhost:5000' + endpoint
data = {'id': 540540540,'message':"h eleftheria goustarei na pinei gala"}
response = requests.post(address,data=data)
if response.status_code==200 :
    print('message trans')

# endpoint='/view_block'
# address = 'http://localhost:5000' + endpoint
# response= requests.get(address)
# print(response.content)