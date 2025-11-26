import requests
import time
import random
import json

# URL Standar MLflow (V1)
url = "http://127.0.0.1:5000/invocations"

print(f"Menembak ke URL: {url}")

def generate_payload():
    # Format Pandas Split (Standar MLflow)
    return {
        "dataframe_split": {
            "columns": [
                "Age", "Gender", "Tenure", "Usage Frequency", "Support Calls", 
                "Payment Delay", "Subscription Type", "Contract Length", 
                "Total Spend", "Last Interaction"
            ],
            "data": [[
                random.randint(18, 65),      # Age
                random.randint(0, 1),        # Gender
                random.randint(1, 60),       # Tenure
                random.randint(1, 30),       # Usage Frequency
                random.randint(0, 10),       # Support Calls
                random.randint(0, 30),       # Payment Delay
                random.randint(0, 2),        # Subscription Type
                random.randint(0, 2),        # Contract Length
                random.uniform(100, 1000),   # Total Spend
                random.randint(1, 30)        # Last Interaction
            ]]
        }
    }

print("Mulai mengirim traffic... (Tekan Ctrl+C untuk stop)")

while True:
    try:
        payload = generate_payload()
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Prediksi Sukses: {response.json()}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"⚠️ Connection Error: {e}")
        
    time.sleep(0.5)