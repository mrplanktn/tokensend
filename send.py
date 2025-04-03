from web3 import Web3
import random

# Konfigurasi Web3
RPC_URL = "https://tea-sepolia.g.alchemy.com/public"  # Ganti dengan RPC URL Anda
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Konfigurasi token dan akun
TOKEN_ADDRESS = "0x90AE3c37E580bD09ba62E87426E8dD68CAd23099"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"  # Ganti dengan private key pengirim
SENDER_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address

# Daftar penerima (contoh)
recipients = [
    "0xRecipientAddress1",
    "0xRecipientAddress2",
    "0xRecipientAddress3"
]

# ABI ERC-20 Transfer function
ERC20_ABI = '[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

# Inisialisasi kontrak token
token_contract = web3.eth.contract(address=TOKEN_ADDRESS, abi=ERC20_ABI)

def send_tokens():
    nonce = web3.eth.get_transaction_count(SENDER_ADDRESS)
    for recipient in recipients:
        amount = random.randint(1, 100) * (10 ** 18)  # Token memiliki 18 desimal
        tx = token_contract.functions.transfer(recipient, amount).build_transaction({
            'from': SENDER_ADDRESS,
            'gas': 200000,
            'gasPrice': web3.to_wei('10', 'gwei'),
            'nonce': nonce
        })
        
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Sent {amount / (10 ** 18)} tokens to {recipient}. TX Hash: {web3.to_hex(tx_hash)}")
        
        nonce += 1  # Increment nonce after each transaction

send_tokens()
