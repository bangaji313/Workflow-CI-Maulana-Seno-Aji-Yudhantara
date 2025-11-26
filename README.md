# MLOps Workflow: CI/CD & Monitoring System

![Python](https://img.shields.io/badge/Python-3.12.7-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Build%20%26%20Push-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Automated-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Visualization-F46800?style=for-the-badge&logo=grafana&logoColor=white)

Repository ini merupakan bagian dari **Kriteria 3 (Workflow CI)** dan **Kriteria 4 (Monitoring)** untuk Submission Proyek Akhir Kelas **"Membangun Sistem Machine Learning"** di Dicoding Indonesia.

Fokus utama repository ini adalah **Deployment** dan **Operasional (Ops)**. Di sini diterapkan pipeline CI/CD otomatis untuk mengemas model menjadi Docker Image, serta sistem monitoring komprehensif untuk memantau kesehatan dan performa model di lingkungan produksi (*serving*).

## 📋 Daftar Isi
- [Arsitektur Sistem](#-arsitektur-sistem)
- [Fitur Utama](#-fitur-utama)
- [Struktur Repository](#-struktur-repository)
- [Pipeline CI/CD](#-pipeline-cicd)
- [Sistem Monitoring](#-sistem-monitoring)
- [Cara Menjalankan](#-cara-menjalankan)

## 🏗️ Arsitektur Sistem
Proyek ini mengintegrasikan berbagai *tools* MLOps modern:
1.  **GitHub Actions:** Mengorkestrasi seluruh proses otomatisasi.
2.  **MLflow Project:** Standarisasi lingkungan pelatihan model.
3.  **DagsHub:** Penyimpanan eksperimen dan *artifact* model (remote tracking).
4.  **Docker Hub:** Registry untuk menyimpan *image* model yang siap *deploy*.
5.  **Prometheus:** Mengumpulkan metrik (*scraping*) dari model.
6.  **Grafana:** Visualisasi metrik dan sistem peringatan (*alerting*).

## 🚀 Fitur Utama

### 1. CI/CD Pipeline (Level Advanced)
Setiap kali ada perubahan kode (*push*), GitHub Actions akan:
- Menyiapkan environment Python & Dependensi.
- Menjalankan pelatihan ulang model (*Retraining*).
- Mengambil *Run ID* model terbaik dari DagsHub.
- Membuat **Docker Image** berisi model tersebut secara otomatis.
- Mengirim (*Push*) Docker Image ke **Docker Hub**.

### 2. Monitoring & Alerting (Level Advanced)
Sistem monitoring "Gaya Sultan" dengan kapabilitas:
- **Prometheus Exporter:** Script khusus (`prometheus_exporter.py`) untuk mengekspos metrik kustom.
- **Grafana Dashboard:** Menampilkan **10+ Metrik** berbeda (Request Rate, Latency, Memory Usage, GC Collection, dll).
- **Alerting System:** **3 Aturan Alert** aktif untuk mendeteksi:
    - *High Traffic* (Lonjakan permintaan).
    - *Churn Prediction Drift* (Hasil prediksi mencurigakan).
    - *Performance Issue* (Masalah memori/latency).

## 📂 Struktur Repository
```text
Workflow-CI-Maulana-Seno-Aji-Yudhantara/
├── .github/workflows/
│   └── main.yml                 # Definisi CI/CD Pipeline
├── credit_scoring_project/      # MLflow Project (Training Code)
│   ├── data/                    # Dataset siap pakai
│   ├── MLproject                # Konfigurasi Entry Point
│   ├── conda.yaml               # Definisi Environment
│   └── modelling.py             # Script Training & Logging
├── Monitoring_Logging/          # Modul Monitoring
│   ├── prometheus.yml           # Konfigurasi Prometheus
│   ├── prometheus_exporter.py   # Script Exporter & Traffic Simulator
│   └── traffic_generator.py     # Script uji beban (Load Test)
└── README.md                    # Dokumentasi
```

## 🔄 Pipeline CI/CD
Workflow didefinisikan dalam .github/workflows/main.yml. Tahapan:
1. Build & Train: Melatih model menggunakan data terbaru.
2. Generate Dockerfile: MLflow membuat instruksi Docker secara otomatis.
3. Build Image: Membangun container image yang lean (ramping).
4. Push to Hub: Upload ke Docker Hub (<username>/credit-scoring-model:latest).

## 📊 Sistem Monitoring (Lokal)
Karena keterbatasan resource cloud gratis, monitoring dijalankan secara lokal menggunakan arsitektur berikut:
1. Model Serving: Model dijalankan via mlflow models serve atau Docker Container.
2. Exporter: prometheus_exporter.py bertindak sebagai middleware untuk menangkap request dan menyediakan endpoint /metrics.
3. Prometheus: Melakukan scraping data tiap 2-5 detik.
4. Grafana: Menampilkan dashboard real-time.

Daftar Alert yang Diterapkan:
- ✅ Traffic Detection Alert: Bunyi jika ada request masuk.
- ✅ High Churn Prediction: Bunyi jika model memprediksi Churn terlalu sering.
- ✅ Slow Scrape/Memory Alert: Bunyi jika ada indikasi masalah performa.

## 💻 Cara Menjalankan (Replikasi Lokal)
1. Persiapan Environment
Pastikan Python 3.12.7, Prometheus, dan Grafana sudah terinstall.
2. Menjalankan Model & Exporter
```bash
# Terminal 1: Serving Model
cd credit_scoring_project
# (Set Environment Variable DagsHub terlebih dahulu)
mlflow models serve -m "runs:/<RUN_ID>/random_forest_model" -p 5000 --no-conda

# Terminal 2: Jalankan Exporter & Traffic Generator
python Monitoring_Logging/prometheus_exporter.py
```
3. Menjalankan Monitoring Stack
- Prometheus: Jalankan dengan config Monitoring_Logging/prometheus.yml.
- Grafana: Import Dashboard JSON dan sambungkan ke Prometheus Data Source (http://localhost:9090).

> Author: Maulana Seno Aji Yudhantara Mahasiswa Informatika - Institut Teknologi Nasional Bandung
