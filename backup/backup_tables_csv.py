import os
import pandas as pd
import mysql.connector
import subprocess
from datetime import datetime

# --- Configuration MySQL ---
DB_NAME = "db_kolenda"
DB_USER = "root"
DB_PASS = "KalanaKa@1212s"
DB_HOST = "127.0.0.1"

# --- Chemin projet et dossier backup ---
BASE_DIR = "/root/kalana/diaffrin"
BACKUP_DIR = os.path.join(BASE_DIR, "backup")
os.makedirs(BACKUP_DIR, exist_ok=True)

# --- Tables à exporter ---
tables = ["diaffrin_api_entitymodel", "diaffrin_api_mouvement", "diaffrin_api_paiement","diaffrin_api_impot"]

# --- Fonction pour supprimer CSV ---
def remove_csv_files():
    for table in tables:
        path = os.path.join(BACKUP_DIR, f"{table}.csv")
        if os.path.exists(path):
            os.remove(path)


remove_csv_files()
# --- Connexion MySQL et export CSV ---
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)

for table in tables:
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    csv_file = os.path.join(BACKUP_DIR, f"{table}.csv")
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")

conn.close()

# --- Git operations ---
try:
    subprocess.run("git fetch origin", shell=True, cwd=BASE_DIR, check=True)

    # Supprimer les anciens CSV avant checkout


    # Checkout ou créer la branche backup_table
    subprocess.run("git checkout -B backup_table", shell=True, cwd=BASE_DIR, check=True)

    # Ajouter et commit les nouveaux CSV
    subprocess.run(f"git add {BACKUP_DIR}", shell=True, cwd=BASE_DIR, check=True)
    msg = f'Backup CSV automatique {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    subprocess.run(f'git commit -m "{msg}" || true', shell=True, cwd=BASE_DIR, check=False)

    # Push sur la branche backup_table
    subprocess.run("git push -u origin backup_table --force", shell=True, cwd=BASE_DIR, check=True)

    # Supprimer les CSV générés avant de revenir sur master
    remove_csv_files()

    # Retour sur master
    subprocess.run("git checkout -f master", shell=True, cwd=BASE_DIR, check=True)

except :
   pass
