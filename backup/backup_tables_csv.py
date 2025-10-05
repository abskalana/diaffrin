import os
import pandas as pd
import mysql.connector
import subprocess
# --- Configuration MySQL ---
DB_NAME = "db_kolenda"
DB_USER = "root"
DB_PASS = "KalanaKa@1212s"
DB_HOST = "127.0.0.1"

# --- Chemin projet et dossier backup ---
BASE_DIR = "/root/kalana/diaffrin"  # chemin vers ton projet
BACKUP_DIR = os.path.join(BASE_DIR, "backup")
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

# --- Exporter chaque table en CSV ---
for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    csv_file = os.path.join(BACKUP_DIR, f"{table}.csv")
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    print(f"Table {table} sauvegardée dans {csv_file}")

cursor.close()
conn.close()

# --- Git commit sur branche backup ---

try:
    # Aller sur la branche backup
    subprocess.run("git fetch origin", shell=True, cwd=BASE_DIR, check=True)
    subprocess.run("git checkout backup", shell=True, cwd=BASE_DIR, check=True)

    # Ajouter les fichiers du backup
    subprocess.run(f"git add {BACKUP_DIR}", shell=True, cwd=BASE_DIR, check=True)

    # Commit avec message horodaté
    subprocess.run('git commit -m "Backup CSV automatique', shell=True, cwd=BASE_DIR, check=True)

    # Push sur la branche backup
    subprocess.run("git push origin backup", shell=True, cwd=BASE_DIR, check=True)

    # Retour sur master
    subprocess.run("git checkout master", shell=True, cwd=BASE_DIR, check=True)

    print("Backup poussé sur branche 'backup' sans affecter master")

except :
    pass

