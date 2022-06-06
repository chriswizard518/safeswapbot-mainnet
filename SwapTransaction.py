# -*- coding: utf-8 -*-
# import threading
import time
# import winsound
from os import system
from bs4 import BeautifulSoup as bsp
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
from web3 import Web3
# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from BuyTokens import buyTokens
# from CommandPromptVisuals import changeCmdPosition
from ThreadingWithReturn import ThreadWithResult
from abi2 import tokenAbi
from sendWhatsappMessage import sendMessage
import config as config
from decimalData2 import getTokenDecimal

bsc = config.BSC_NET

web3 = Web3(Web3.HTTPProvider(bsc))
if web3.isConnected(): print("Connected to BSC")

# User Input Address for Token
if bool(config.TRADE_TOKEN_ADDRESS):
    address = config.TRADE_TOKEN_ADDRESS
else:
    address = input('Enter token address: ')

# Important Addresses
TokenToSellAddress = web3.toChecksumAddress(address)
WBNB_Address = web3.toChecksumAddress(config.WBNB_ADDRESS)
safeswapRouterAddress = web3.toChecksumAddress(config.SAFESWAP_ROUTER_ADDRESS)
walletAddress = config.YOUR_WALLET_ADDRESS
TradingTokenDecimal = None

# To clear command line
# clear = lambda: system("cls")
# options = Options()
# options.headless = True
# options.add_argument("--enable-javascript")
wallet_bnb_limit = float(input(f"Enter amount of BNB limit on you want to left(Default: 0): "))
oneTimeBNBAmount = float(input(f"Enter amount of BNB amount per transaction(Default: 3.2): "))

def showTx(url):
    webdriver.Chrome(executable_path=ChromeDriverManager().install()).get(url)

def InitializeTrade():
    global TokenToSellAddress
    global TradingTokenDecimal
    # Getting ABI
    sellTokenAbi = tokenAbi(TokenToSellAddress)
    safeAbi = tokenAbi(safeswapRouterAddress)

    # Enter you wallet Public Address
    BNB_balance = web3.eth.get_balance(walletAddress)
    BNB_balance = web3.fromWei(BNB_balance, 'ether')
    # print(f"Current BNB Balance: {web3.fromWei(BNB_balance, 'ether')}")

    # Create a contract for both safeRoute and Token to Sell
    contractRouter = web3.eth.contract(address=safeswapRouterAddress, abi=safeAbi)
    contractSellToken = web3.eth.contract(TokenToSellAddress, abi=sellTokenAbi)
    if TradingTokenDecimal is None:
        TradingTokenDecimal = contractSellToken.functions.decimals().call()
        TradingTokenDecimal = getTokenDecimal(TradingTokenDecimal)
        
    NoOfTokens = contractSellToken.functions.balanceOf(walletAddress).call()
    NoOfTokens = web3.fromWei(NoOfTokens, TradingTokenDecimal)
    symbol = contractSellToken.functions.symbol().call()

    if BNB_balance <= oneTimeBNBAmount:
        toBuyBNBAmount = float(BNB_balance) - 0.02
    else:
        toBuyBNBAmount = oneTimeBNBAmount
                
    params = {
        'symbol': symbol,
        'web3': web3,
        'walletAddress': walletAddress,
        'contractSellToken': contractSellToken,
        'contractRouter': contractRouter,
        'safeswapRouterAddress': safeswapRouterAddress,
        'TokenToSellAddress': TokenToSellAddress,
        'WBNB_Address': WBNB_Address,
        'TradingTokenDecimal': TradingTokenDecimal,
        'toBuyBNBAmount': toBuyBNBAmount
    }

    return BNB_balance, symbol, NoOfTokens, params

def runCode():
    print(".................Swap is starting..........")
    dataEntered = False
    Lasttrade_message = None
    tx = None
    trade_num = 0
    while True:
        print(f"\n\n=========trade number ={trade_num}===========")

        if not dataEntered:
            BNB_balance, TokenSymbol, NoOfTokens, params = InitializeTrade()

        print(f"Token name: {TokenSymbol}")
        print(f"Total avaliable {TokenSymbol}: {NoOfTokens}")
        print(f"Account BNB balance: {BNB_balance}")

        if BNB_balance <= wallet_bnb_limit + 0.02:
            print("\n ***bnb amount reached to limitation, swap is over***")
            print("......The End.......")
            break

        tradeMode ='buy'        
        if tradeMode == 'buy':
            p3 = ThreadWithResult(target=buyTokens, kwargs=params)
            p3.start()
            p3.join()

            tx, Lasttrade_message = p3.result
            print(Lasttrade_message);
            print(f"Tx : https://bscscan.com/tx/{tx}\n")
            
            # if  "Failed" not in tx and config.SHOW_TX_ON_BROWSER:
            #     showTx(f"https://testnet.bscscan.com/tx/{tx}")
            #     # showTx(f"https://bscscan.com/tx/{tx}")
            #     time.sleep(6)   
            if  "Failed" in tx:
                print("........Swap was stopped.........")
                break                                   
                
        else:
            print("Invalid Input")
            time.sleep(2)
            print("Restarting Program")
            time.sleep(1)
            print(".");
            time.sleep(1)
            print("..");
            time.sleep(1)
            print("...");
            time.sleep(1)
            runCode()
        time.sleep(16)
        trade_num += 1
        # clear()


if __name__ == "__main__":
    runCode()
