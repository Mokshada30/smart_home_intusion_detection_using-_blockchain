import pandas as pd
import joblib
import requests
import time
import random
import os

# --- CONFIGURATION ---
FLASK_API_URL = "http://127.0.0.1:5000/log_intrusion"
MODEL_PATH = 'models/intrusion_model.pkl'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# --- THIS IS THE FIX ---
# Point to our new, pre-shuffled, smaller sample file
SAMPLE_DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'monitor_sample.csv')
# --- END OF FIX ---

def run_monitor():
    try:
        print(f"Loading intrusion model from {MODEL_PATH}...")
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully.")
    except Exception as e:
        print(f"❌ ERROR: Could not load model '{MODEL_PATH}'.")
        print(f"   -> Details: {e}")
        return

    try:
        print(f"Loading SHUFFLED sample data from {SAMPLE_DATA_PATH}...")
        # No more nrows=1000, we load the whole 200k sample file
        df_sample = pd.read_csv(SAMPLE_DATA_PATH) 
        
        features = model.feature_names_in_
        X_sample = df_sample[features]
        
        if 'device' not in df_sample.columns:
             print("   -> 'device' column not found. Using placeholder.")
        
        print("✅ Sample data loaded.")
    except Exception as e:
        print(f"❌ ERROR: Could not load data from {SAMPLE_DATA_PATH}.")
        print(f"   -> Have you run 'train_model.py' to create this file?")
        print(f"   -> Details: {e}")
        return

    print("\n--- 🚀 Starting Real-Time Monitoring Simulation ---")
    print("Will predict one event every 3-5 seconds. Press Ctrl+C to stop.")

    try:
        while True:
            idx = random.randint(0, len(X_sample) - 1)
            single_event_features = X_sample.iloc[[idx]]
            
            if 'device' in df_sample.columns:
                device = df_sample.iloc[idx]['device']
            else:
                device = "Unknown_Device"
            
            prediction = model.predict(single_event_features)[0] 
            
            try:
                intrusion_flag = int(prediction) 
            except ValueError:
                intrusion_flag = 1 if 'attack' in str(prediction).lower() else 0
            
            status = "INTRUSION" if intrusion_flag == 1 else "Benign"
            
            # This is the color-coding for your terminal!
            if intrusion_flag == 1:
                print(f"\n\033[91mDevice: {device} | Status: {status}\033[0m") # Red
            else:
                print(f"\nDevice: {device} | Status: {status}") # Default color
            
            try:
                payload = {"device": device, "intrusion": intrusion_flag}
                response = requests.post(FLASK_API_URL, json=payload)
                
                if response.status_code == 200:
                    tx_hash = response.json().get('tx_hash', 'N/A')
                    print(f"  -> Logged to blockchain. TX: {tx_hash[:10]}...")
                else:
                    print(f"  -> ERROR: Failed to log to API. Status: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print("  -> ❌ ERROR: Could not connect to Flask API. Is app.py running?")

            time.sleep(random.randint(3, 5))

    except KeyboardInterrupt:
        print("\n--- 🛑 Monitoring Stopped ---")

if __name__ == "__main__":
    run_monitor()