import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
import dagshub
import os

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay

# 1. KONFIGURASI DAGSHUB
DAGSHUB_USERNAME = os.environ.get("DAGSHUB_USERNAME") 
DAGSHUB_TOKEN = os.environ.get("DAGSHUB_TOKEN")
REPO_NAME = "Eksperimen_SML_Maulana-Seno-Aji-Yudhantara"

# Setup otentikasi DagsHub via Environment Variable
os.environ["MLFLOW_TRACKING_USERNAME"] = DAGSHUB_USERNAME
os.environ["MLFLOW_TRACKING_PASSWORD"] = DAGSHUB_TOKEN

# URL Tracking DagsHub (Format: https://dagshub.com/<username>/<repo>.mlflow)
mlflow.set_tracking_uri(f"https://dagshub.com/bangaji313/Eksperimen_SML_Maulana-Seno-Aji-Yudhantara.mlflow")

print("Menghubungkan ke DagsHub...")
# dagshub.init(repo_owner=DAGSHUB_USERNAME, repo_name=REPO_NAME, mlflow=True)
mlflow.set_experiment("Eksperimen Churn Prediction - CI/CD")

# 2. LOAD DATA
# Ambil data yang sudah dibersihkan dari Kriteria 1
data_path = '../preprocessing/customer_churn_cleaned.csv'

if not os.path.exists(data_path):
    print(f"Error: File {data_path} tidak ditemukan. Jalankan automate script dulu!")
    exit()

print("Loading dataset...")
df = pd.read_csv(data_path)

# Pisahkan Fitur (X) dan Target (y)
X = df.drop(columns=['Churn'])
y = df['Churn']

# Split Train & Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. HYPERPARAMETER TUNING (Syarat Skilled)
print("Memulai Hyperparameter Tuning...")

# Kita pakai Random Forest
rf = RandomForestClassifier(random_state=42)

# Grid Search (Mencari kombinasi terbaik)
param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5]
}

grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
best_params = grid_search.best_params_

print(f"Parameter Terbaik: {best_params}")

# 4. EVALUASI MODEL
y_pred = best_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"Akurasi Model: {accuracy}")

# 5. LOGGING KE MLFLOW/DAGSHUB
print("Mengirim report ke DagsHub...")

# Tambahkan "as run" untuk menangkap ID sesi training
with mlflow.start_run() as run:
    # A. Log Parameters
    mlflow.log_params(best_params)
    
    # B. Log Metrics
    mlflow.log_metrics({
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    })
    
    # C. Log Model
    mlflow.sklearn.log_model(best_model, "random_forest_model")
    
    # D. Simpan Run ID ke file teks (PERLU)
    run_id = run.info.run_id
    with open("run_id.txt", "w") as f:
        f.write(run_id)
    print(f"Run ID ({run_id}) tersimpan di run_id.txt")

    # E. Log Artefak Tambahan
    print("Membuat Artefak 2: Feature Importance...")
    plt.figure(figsize=(10, 6))
    importances = best_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    plt.title("Feature Importances")
    plt.bar(range(X.shape[1]), importances[indices], align="center")
    plt.xticks(range(X.shape[1]), X.columns[indices], rotation=90)
    plt.tight_layout()
    plt.savefig("feature_importance.png")
    mlflow.log_artifact("feature_importance.png")
    
    print("Selesai! Cek DagsHub kamu.")