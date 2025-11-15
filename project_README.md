Blockchain-Enabled Intrusion Detection for Smart Homes

This is a full-stack application that uses a Machine Learning model to detect network intrusions in real-time and logs these events to a secure, immutable Ethereum blockchain. A web dashboard provides a live, on-chain view of all security events.

This system is designed to solve the "log tampering" problem: even if an attacker gains access to the server, they cannot alter or delete the security logs that have been recorded on the blockchain.

Core Features

High-Accuracy ML Model: A RandomForestClassifier trained on the N-BaIoT dataset to detect intrusions with 99.99% accuracy.

Immutable Ledger: A Solidity Smart Contract (IntrusionLog.sol) deployed on a local Ganache blockchain ensures all logs are tamper-proof.

Full-Stack Application:

A Flask API (app.py) serves as the central nervous system.

A Web Dashboard (frontend/index.html) provides a real-time, user-friendly view of on-chain logs.

An Automated Monitor (monitor.py) simulates live traffic, makes ML predictions, and automatically logs events.

How It Works: Data Flow

The system operates in a continuous loop:

[Simulate] monitor.py loads the trained ML model (models/intrusion_model.pkl) and a sample data file (data/monitor_sample.csv).

[Predict] It picks a random event from the data, and the ML model predicts if it's an "Intrusion" (1) or "Benign" (0).

[Log] It sends this prediction (e.g., {"device": "Baby_Monitor", "intrusion": 1}) to the Flask API's /log_intrusion endpoint.

[Secure] The Flask server (app.py) calls the logIntrusion() function on the Smart Contract, using the address and ABI from the config files.

[Record] The Smart Contract permanently records the event (device, timestamp, block number) in a new block on the Ganache chain. This action is immutable.

[Display] The web dashboard (in the user's browser) calls the Flask /get_logs API, which reads all events from the Smart Contract and displays them in the table.

1. Required Installations

Software

Python (3.10+ recommended)

Git (for cloning the repository)

Ganache: A local Ethereum blockchain. Download it from TruffleSuite.

Remix IDE (Web): Used to compile and deploy the smart contract. Access it at remix.ethereum.org.

Python Libraries

This repository includes a requirements.txt file. You can install all Python dependencies with a single command:

# After cloning, run this in your project's root directory
pip install -r requirements.txt


2. Setup Guide (Step-by-Step)

Follow these instructions in order to get the project running from scratch.

Step 1: Clone the Repository

git clone [https://github.com/Mokshada30/smart_home_intusion_detection_using-_blockchain.git](https://github.com/Mokshada30/smart_home_intusion_detection_using-_blockchain.git)
cd smart_home_intusion_detection_using-_blockchain


Step 2: Install Python Libraries

pip install -r requirements.txt


Step 3: Get the Dataset (CRITICAL)

This repository does not include the data, as the files are several gigabytes in size. You must acquire the dataset and place it in the correct folder.

Download: The project uses the N-BaIoT dataset. You can find it here: UNB N-BaIoT Dataset Page.
https://www.kaggle.com/datasets/mkashifn/nbaiot-dataset

Unzip: Unzip the main file. You will have a folder containing 89 .csv files for 9 different IoT devices.

Create Folder: In the project's root directory (the smart_home_intusion_detection_using-_blockchain folder), create a new folder named data.

Move Files: Move all 89 CSV files into the data/ folder you just created.

Your project structure should now look like this:

smart_home_intusion_detection_using-_blockchain/
├── data/
│   ├── 1.philips_B120N10.csv
│   ├── 2.danmini_doorbell.csv
│   ├── ... (and 87 more .csv files)
├── frontend/
├── scripts/
└── ...


Step 4: Run One-Time Setup Scripts

These scripts preprocess your data and train the ML model. You only need to do this once.

Preprocess Data: This script reads all 89 CSVs and combines them into one large file (data/combined_nbaiot.csv).

python scripts/preprocess_nbaiot.py


Train the ML Model: This script loads the combined data, trains the model, and creates two essential files:

models/intrusion_model.pkl (The trained "brain")

data/monitor_sample.csv (The shuffled sample for the monitor)

python scripts/train_model.py


Step 5: Deploy Your Smart Contract

This is the most manual step.

Start Ganache: Open the Ganache application. A new "QUICKSTART" workspace is perfect.

Open Remix: Go to remix.ethereum.org.

Paste Code: Copy the code from scripts/IntrusionLog.sol and paste it into a new file (e.g., IntrusionLog.sol) in Remix.

Compile:

Go to the "Solidity Compiler" tab.

Set the Compiler to a 0.8.x version (e.g., 0.8.18).

Click "Advanced Configurations" and set EVM Version to london. (This is a critical bug fix!)

Click "Compile".

Deploy:

Go to the "Deploy & Run Transactions" tab.

Set the Environment to "Ganache Provider". (It will ask for http://127.0.0.1:7545, which is correct).

Click the orange "Deploy" button.

Update Config Files: After it deploys, you must update the config files in the scripts/ folder:

Address: In Remix, click the "Copy" icon next to your deployed contract address. Paste this entire address into scripts/contract_address.txt, replacing its contents.

ABI: In Remix, go back to the "Compiler" tab and click the "ABI" button. Paste this entire JSON ABI into scripts/contract_abi.json, replacing its contents.

3. How to Run the Full Demo

You are now ready to run the full application!

Run Blockchain: Make sure Ganache is open and running.

Run Server: In your first terminal, start the Flask API server:

python scripts/app.py


Open Dashboard: In your web browser, go to http://127.0.0.1:5000. You should see the empty dashboard.

Run Monitor: In a second terminal, start the ML monitoring script:

python scripts/monitor.py


Watch: Look at your second terminal as it predicts "Benign" and "INTRUSION" events. Refresh your browser dashboard to see the new logs appear in real-time, complete with their block numbers!
