import csv
import os
import json
from datetime import datetime
from django.conf import settings

def append_to_csv(filename, data, folder="data"):

    try:
        if not data:
            return  # Rien à écrire si data est vide

        # Crée le chemin du dossier à la racine du projet
        folder_path = os.path.join(settings.BASE_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)  # Crée le dossier si nécessaire

        # Chemin complet du fichier CSV
        file_path = os.path.join(folder_path, filename)
        file_exists = os.path.isfile(file_path)

        with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
            if isinstance(data, list):
                keys = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                if not file_exists:
                    writer.writeheader()
                for item in data:
                    writer.writerow(item)
            else:
                keys = data.keys()
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)

    except :
       pass



def append_to_txt(filename, errors, mdata=None, folder="data"):

    try:
        # Crée le chemin du dossier à la racine du projet
        folder_path = os.path.join(settings.BASE_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)

        # Chemin complet du fichier TXT
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.now()} ---\n")
            if mdata is not None:
                f.write("Data:\n")
                f.write(json.dumps(mdata, ensure_ascii=False, indent=2))
                f.write("\n")
            f.write("Errors:\n")
            f.write(json.dumps(errors, ensure_ascii=False, indent=2))
            f.write("\n-------------------------\n")
    except:
        pass
