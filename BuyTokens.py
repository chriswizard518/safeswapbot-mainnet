import config
import time

def buyTokens(**kwargs):
    symbol = kwargs.get('symbol')
    web3 = kwargs.get('web3')
    walletAddress = kwargs.get('walletAddress')
    contractRouter = kwargs.get('contractRouter')
    TokenToBuyAddress = kwargs.get('TokenToSellAddress')
    WBNB_Address = kwargs.get('WBNB_Address')

    # toBuyBNBAmount = input(f"Enter amount of BNB you want to buy {symbol}: ")
    toBuyBNBAmount = kwargs.get('toBuyBNBAmount')
    toBuyBNBAmount = web3.toWei(toBuyBNBAmount, 'ether')

    #BSC testnet gas fee settings
    
    # safeSwap_txn = contractRouter.functions.swapExactETHForTokens(0,
    #                                                                   [WBNB_Address, TokenToBuyAddress],
    #                                                                   walletAddress,
    #                                                                   (int(time.time() + 10000))).buildTransaction({
    #     'from': walletAddress,
    #     'value': toBuyBNBAmount,  # Amount of BNB
    #     'gas': 420000,
    #     'gasPrice': web3.toWei('10', 'gwei'),
    #     'nonce': web3.eth.get_transaction_count(walletAddress)
    # })  
    
    
    #BSC maintnet gas fee settings
       
    safeSwap_txn = contractRouter.functions.swapExactETHForTokens(0,
                                                                      [WBNB_Address, TokenToBuyAddress],
                                                                      walletAddress,
                                                                      (int(time.time() + 10000))).buildTransaction({
        'from': walletAddress,
        'value': toBuyBNBAmount,  # Amount of BNB
        'gas': 2701884,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(walletAddress)
    })  
                                                                      
    signed_txn = web3.eth.account.sign_transaction(safeSwap_txn, private_key=config.YOUR_PRIVATE_KEY)
    tx_hash = web3.toHex(web3.keccak(signed_txn.rawTransaction))

    
    try:
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        result = [web3.toHex(tx_token), f"Bought {web3.fromWei(toBuyBNBAmount, 'ether')} BNB of {symbol}"]
        return result
    except ValueError as e:
        print("exception============")
        if e.args[0].get('message') in 'intrinsic gas too low':
            result = ["Failed", f"ERROR: {e.args[0].get('message')}"]
            # print("first error")
            # print("result=", result)
        else:
            result = ["Failed", f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"]
            # print("else error")
            # print("result=", result)
        return result

