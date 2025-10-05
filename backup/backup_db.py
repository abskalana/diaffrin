import os
import pandas as pd
import mysql.connector
import subprocess
from datetime import datetime

# --- Configuration ---
DB_NAME = "db_kolenda"
DB_USER = "root"
DB_PASS = "KalanaKa@1212s"
DB_HOST = "127.0.0.1"
BACKUP_DIR = "backup"  # dossier fixe pour écraser à chaque fois

# --- Crée le dossier backup s'il n'existe pas ---
os.makedirs(BACKUP_DIR, exist_ok=True)

# --- Connexion à MySQL ---
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)

cursor = conn.cursor()

# --- Récupérer toutes les tables ---
cursor.execute("SHOW TABLES")
tables = [row[0] for row in cursor.fetchall()]

# --- Exporter chaque table en CSV dans le dossier backup (écrase les fichiers existants) ---
for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    csv_file = os.path.join(BACKUP_DIR, f"{table}.csv")
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")

cursor.close()
conn.close()

# --- Git add / commit / push ---
date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
try:
    subprocess.run("git add backup/", shell=True, check=True)
    subprocess.run(f'git commit -m "Backup CSV automatique {date_str}"', shell=True, check=True)
    subprocess.run("git push origin main", shell=True, check=True)
except subprocess.CalledProcessError:
