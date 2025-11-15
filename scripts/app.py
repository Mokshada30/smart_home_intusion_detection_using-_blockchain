from flask import Flask, request, jsonify, render_template
from web3 import Web3
import json
import os

# --- Configuration ---
# Set paths relative to this script's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'frontend')
ABI_PATH = os.path.join(BASE_DIR, 'contract_abi.json')
ADDRESS_PATH = os.path.join(BASE_DIR, 'contract_address.txt')
# --- End Configuration ---

# Tell Flask where to find the 'frontend' folder
app = Flask(__name__, template_folder=TEMPLATE_DIR)

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

if not w3.is_connected():
    raise Exception("Failed to connect to Ganache")

account = w3.eth.accounts[0]

# --- Load Contract Details from Files (No more hard-coding!) ---
try:
    print("Loading contract configuration...")
    # Load Address
    with open(ADDRESS_PATH, 'r') as f:
        contract_address = f.read().strip() # .strip() removes any newlines
    
    # Load ABI
    with open(ABI_PATH, 'r') as f:
        abi = json.load(f)

    print(f"Loaded contract at address: {contract_address}")
    contract = w3.eth.contract(address=contract_address, abi=abi)

except FileNotFoundError as e:
    print(f"❌ CRITICAL ERROR: Could not find config file.")
    print(f"   -> Details: {e}")
    print("   -> Make sure 'contract_abi.json' and 'contract_address.txt' exist in the 'scripts' folder.")
    exit()
# --- End Contract Load ---


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_logs', methods=['GET'])
def get_logs():
    try:
        total_logs = contract.functions.getEventsCount().call()
        all_logs = []

        for i in range(total_logs - 1, -1, -1):
            log_data = contract.functions.getEvent(i).call()
            
            all_logs.append({
                "id": i,
                "device": log_data[0],
                "timestamp": log_data[1], 
                "intrusion": "Yes" if log_data[2] == 1 else "No",
                "blockNum": log_data[3]
            })
        
        return jsonify(all_logs)
    
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/log_intrusion', methods=['POST'])
def log_intrusion():
    data = request.json
    device_name = data['device']
    intrusion_flag = int(data['intrusion'])

    try:
        tx = contract.functions.logIntrusion(device_name, intrusion_flag).transact({'from': account})
        receipt = w3.eth.wait_for_transaction_receipt(tx)

        return jsonify({
            "message": "Intrusion logged successfully!",
            "tx_hash": receipt.transactionHash.hex()
        })
    except Exception as e:
        print(f"Error logging intrusion: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)