import json
import requests
import time
import sys

headers = {'User':'be8fc95242bc59217dd8d606'}
##Fetch LPs
r = ''
try:
	r = requests.get('http://axon.while0x1.com:8090/lps', headers=headers)
except Exception as e:
	print(e)
    print('Requests Error')

if r != '':
	LPs =  r.json()
	print('Available LPs:')
	for dex in LPs:
		print(dex)
		for pair in LPs[dex]:
			print(f'    {pair} ')	
			time.sleep(0.2)
   
#Fetch Specific Dex/LP Statistics
data = {'dex':'minswap','pair': 'ADA-MIN','swap_asset': 'lovelace', 'swap_amount': 10000000}
r = ''
try:
	r = requests.post('http://axon.while0x1.com:8090/poolinfo', headers=headers,json=data)
except Exception as e:
    print('Request failed')
    print(e)
    sys.exit()  
if r !='':
    print(r.json())
#Create a Swap - returns usigned transaction CBOR
# Address must contain a stake-key
data = {'dex':'minswap','pair': 'ADA-MIN', 'address': 'addr1q8qev5chh7me46y5gskrmjeawyunullgpzm6suzzf8vkshnzn3esu8nuwh0frr83sv9qgv29540vhdtxrf5hlhxs0yzqdme4ec', 'swap_asset': 'lovelace', 'swap_amount': 5000000}
r = ''
try:
	r = requests.post('http://axon.while0x1.com:8090/swap', headers=headers,json=data)
except Exception as e:
    print('Request failed')
    print(e)
    sys.exit() 
if r != '':    
    print(r.json())
    
#donations
#addr1vy69dh482jjpwew7m6vz44q2y8w855gt58n0f9dc76zfhwcardan0
