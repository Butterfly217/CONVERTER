from web3 import Web3

# Sample connection to Sepolia or any testnet/local chain
def connect_wallet():
    try:
        infura_url = "https://sepolia.infura.io/v3/e91b2e6612bf454e953ea77ddc36e736"
        w3 = Web3(Web3.HTTPProvider(infura_url))

        if w3.is_connected():
            return True
        return False
    except Exception as e:
        print("Web3 error:", e)
        return False
