import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .constant import STATUS_CHOICES_LIST,STATUS_CHOICES_LIST_NON_PAYE,STATUS_CHOICES_LIST_PAYE

def validate_date_range(value):
    today = timezone.now().date()
    min_date = today - datetime.timedelta(days=10)
    max_date = today + datetime.timedelta(days=10)

    if value < min_date:
        raise ValidationError(f"La date ne peut pas être antérieure à {min_date.strftime('%d/%m/%Y')}.")
    if value > max_date:
        raise ValidationError(f"La date ne peut pas être postérieure à {max_date.strftime('%d/%m/%Y')}.")

def truncate_gps(coord):
    lat, lon = coord.split(";")
    lat = f"{float(lat):.6f}"
    lon = f"{float(lon):.6f}"
    return f"{lat};{lon}"
def to_slug(phone,coord):
    lat, lon = coord.split(";")
    lat = f"{float(lat):.4f}"
    lon = f"{float(lon):.4f}"
    coord = f"{lat}{lon}"
    res = phone.replace(',','')
    txt = coord.replace('.','').replace('-','')
    return slugify(str(res)+str(txt))

def is_active(entity):
    if entity.contact_phone == "12345678" : return False
    t = ("absent","fermer","fermé")
    if entity.contact_prenom.lower() in t and entity.contact_nom.lower() in t: return False
    return True


def get_status(status):
    if not status: return status
    if status in STATUS_CHOICES_LIST: return [status]
    if status.upper() =="NON_PAYÉ": return STATUS_CHOICES_LIST_NON_PAYE
    if status.upper() == "DEJA_PAYÉ": return STATUS_CHOICES_LIST_PAYE
    return STATUS_CHOICES_LIST


def filter_entities_by_status(entities, status_input):
    """
    Filtre une liste d'entités selon le status_input.
    Chaque entité doit posséder l'attribut 'paiement' (None si pas de paiement).

    status_input peut être :
        - "DEJA_PAYÉ"      → paiements PAYÉ / PAYE_MAIRIE
        - "NON_PAYÉ"       → paiements REFUS / FERMÉ / ABSENT / AUTRE
        - "NON_DEMANDÉ"    → uniquement entités sans paiement
        - un status précis  → entités avec paiement exactement ce status
        - vide ou autre    → toutes les entités
    """
    status_upper = status_input.upper() if status_input else ""

    if status_upper == "NON_DEMANDÉ":
        # uniquement entités sans paiement
        return [e for e in entities if e.paiement is None]

    elif status_upper == "NON_PAYÉ":
        # entités avec paiement NON_PAYÉ uniquement
        status_list = STATUS_CHOICES_LIST_NON_PAYE
        return [e for e in entities if e.paiement and e.paiement.status in status_list]

    elif status_upper == "DEJA_PAYÉ":
        # entités avec paiement PAYÉ ou PAYE_MAIRIE
        status_list = STATUS_CHOICES_LIST_PAYE
        return [e for e in entities if e.paiement and e.paiement.status in status_list]

    elif status_upper in STATUS_CHOICES_LIST:
        # entités avec paiement exactement ce status
        return [e for e in entities if e.paiement and e.paiement.status == status_upper]

    # sinon status vide ou "Tous", on garde toutes les entités
    return entities
