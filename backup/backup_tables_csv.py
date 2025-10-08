import os
import pandas as pd
import mysql.connector
import subprocess
from datetime import datetime

DB_NAME = "db_kolenda"
DB_USER = "root"
DB_PASS = "KalanaKa@1212s"
DB_HOST = "127.0.0.1"

# --- Chemin projet et dossier backup ---
BASE_DIR = "/root/kalana/diaffrin"
BACKUP_DIR = os.path.join(BASE_DIR, "backup")
os.makedirs(BACKUP_DIR, exist_ok=True)

# --- Connexion MySQL ---
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)

# --- Tables à exporter ---
tables = ["diaffrin_api_entitymodel", "diaffrin_api_mouvement", "diaffrin_api_paiement"]

# --- Exporter chaque table en CSV ---
for table in tables:
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    csv_file = os.path.join(BACKUP_DIR, f"{table}.csv")
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")

conn.close()

# --- Git commit sur branche backup ---
try:
    subprocess.run("git fetch origin", shell=True, cwd=BASE_DIR, check=True)
    subprocess.run("git checkout backup_table", shell=True, cwd=BASE_DIR, check=True)
    subprocess.run(f"git add {BACKUP_DIR}", shell=True, cwd=BASE_DIR, check=True)

    msg = f'Backup CSV automatique {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    subprocess.run(f'git commit -m "{msg}" || true', shell=True, cwd=BASE_DIR, check=False)

    subprocess.run("git push origin backup_table", shell=True, cwd=BASE_DIR, check=True)

    files_to_remove = [
        "diaffrin_api_entitymodel.csv",
        "diaffrin_api_mouvement.csv",
        "diaffrin_api_paiement.csv"
    ]
    for f in files_to_remove:
        path = os.path.join(BACKUP_DIR, f)
        if os.path.exists(path):
            os.remove(path)

    # Puis safe de revenir sur master
    subprocess.run("git checkout master", shell=True, cwd=BASE_DIR, check=True)

    subprocess.run("git checkout master", shell=True, cwd=BASE_DIR, check=True)

except Exception:
    pass
