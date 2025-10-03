import csv
import os


import csv
import os
from django.conf import settings
import traceback

def append_to_csv(filename, data, folder="data"):
    """
    Ajoute des données dans un fichier CSV dans le dossier `data` à la racine du projet
    sans écraser le fichier. Crée le dossier s'il n'existe pas.
    En cas d'erreur, capture l'exception et continue.

    Args:
        filename (str): Nom du fichier CSV.
        data (dict ou list[dict]): Données à sauvegarder.
        folder (str): Nom du dossier où sauvegarder le fichier (défaut: "data").
    """
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

