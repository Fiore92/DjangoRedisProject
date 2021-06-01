from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/c8417e6fe457452ab1402d681437cea5'))
account=w3.eth.account.create()
privateKey=account.privateKey.hex()
address=account.address

print(f"your address: {address}\n your key: {privateKey}")
#address 0x827F30fcda0dA02F39BA58d3Dc24c70EB1928788
#key 0x5ee177eb18f2c07f9d31d46f1bfb6b52a86918ebc7462946bbfab7334b5a1806