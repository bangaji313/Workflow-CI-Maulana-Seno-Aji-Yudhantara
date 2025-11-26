import time
import requests
import random
from prometheus_client import start_http_server, Summary, Counter, Gauge

# 1. DEFINISI METRIKS PROMETHEUS
# Mengukur waktu proses (Latency)
REQUEST_TIME = Summary('model_request_processing_seconds', 'Time spent processing request')
# Menghitung jumlah request
REQUEST_COUNT = Counter('model_request_total', 'Total request count')
# Mengukur akurasi / prediksi (memakai Gauge untuk dummy)
PREDICTION_VALUE = Gauge('model_prediction_value', 'Prediction output value')

# 2. KONFIGURASI TARGET MODEL
MODEL_URL = "http://127.0.0.1:5000/invocations"

def generate_payload():
    return {
        "dataframe_split": {
            "columns": ["Age", "Gender", "Tenure", "Usage Frequency", "Support Calls", 
                        "Payment Delay", "Subscription Type", "Contract Length", 
                        "Total Spend", "Last Interaction"],
            "data": [[
                random.randint(18, 65), random.randint(0, 1), random.randint(1, 60),
                random.randint(1, 30), random.randint(0, 10), random.randint(0, 30),
                random.randint(0, 2), random.randint(0, 2), random.uniform(100, 1000),
                random.randint(1, 30)
            ]]
        }
    }

# 3. FUNGSI UTAMA (TRAFFIC + MONITORING)
@REQUEST_TIME.time()  # Decorator ini otomatis mengukur durasi fungsi
def process_request():
    try:
        payload = generate_payload()
        headers = {"Content-Type": "application/json"}
        
        # Kirim request ke Model
        response = requests.post(MODEL_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            REQUEST_COUNT.inc() # Tambah counter
            # Ambil hasil prediksi (misal: [1.0])
            pred = response.json()['predictions'][0]
            PREDICTION_VALUE.set(pred) # Update grafik gauge
            print(f"✅ Request Sukses! Prediksi: {pred}")
        else:
            print(f"❌ Error {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Koneksi Gagal: {e}")

if __name__ == '__main__':
    # Jalankan server metrics di port 8082
    print("🚀 Exporter berjalan di http://localhost:8082/metrics")
    start_http_server(8082)
    
    # Loop selamanya untuk generate traffic
    while True:
        process_request()
        time.sleep(1)