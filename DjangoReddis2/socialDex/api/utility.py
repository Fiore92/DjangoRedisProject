from web3 import Web3

def sendTransaction(message):

    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/c8417e6fe457452ab1402d681437cea5'))
    address= '0x827F30fcda0dA02F39BA58d3Dc24c70EB1928788'
    privateKey='0x5ee177eb18f2c07f9d31d46f1bfb6b52a86918ebc7462946bbfab7334b5a1806'
    nonce=w3.eth.getTransactionCount(address)
    gasPrice= w3.eth.gasPrice
    value=w3.toWei(0,'ether')
    signedTx=w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ),privateKey)
    tx=w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId= w3.toHex(tx)
    return txId


