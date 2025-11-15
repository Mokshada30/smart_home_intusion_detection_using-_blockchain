from web3 import Web3
import json
import os

# --- Configuration ---
# Set paths relative to this script's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ABI_PATH = os.path.join(BASE_DIR, 'contract_abi.json')
ADDRESS_PATH = os.path.join(BASE_DIR, 'contract_address.txt')
# --- End Configuration ---


# --- 1️⃣ Connect to Ganache ---
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

if w3.is_connected():
    print("Connected to Ganache ✅")
else:
    raise Exception("Failed to connect to Ganache ❌")

# --- 2️⃣ Set your account ---
account = w3.eth.accounts[0]
print(f"Using account: {account}")

# --- 3️⃣ Load Contract Details from Files ---
try:
    print("Loading contract configuration...")
    # Load Address
    with open(ADDRESS_PATH, 'r') as f:
        contract_address = f.read().strip()
    
    # Load ABI
    with open(ABI_PATH, 'r') as f:
        contract_abi = json.load(f)

    print(f"Loaded contract at address: {contract_address}")
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    print("Contract loaded successfully ✅")

except FileNotFoundError as e:
    print(f"❌ CRITICAL ERROR: Could not find config file.")
    print(f"   -> Details: {e}")
    print("   -> Make sure 'contract_abi.json' and 'contract_address.txt' exist in the 'scripts' folder.")
    exit()
# --- End Contract Load ---


# --- 4️⃣ (Optional test call) ---
# This file can now be imported by other scripts, or you can add test code here.
# For example, to log a single test event:

def log_test_event():
    print("Logging a test event...")
    try:
        tx_hash = contract.functions.logIntrusion("Test_Device_From_Script", 1).transact({'from': account})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"  -> Test event logged! TX: {receipt.transactionHash.hex()}")
        
        count = contract.functions.getEventsCount().call()
        print(f"  -> Total events in contract: {count}")
        
    except Exception as e:
        print(f"  -> ❌ Error logging test event: {e}")

# If you run this file directly, it will log a test event.
if __name__ == "__main__":
    log_test_event()