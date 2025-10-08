import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .constant import *
import uuid

import random, time


def validate_date_range(value):
    today = timezone.now().date()
    min_date = today - datetime.timedelta(days=10)
    max_date = today + datetime.timedelta(days=10)

    if value < min_date:
        raise ValidationError(f"La date ne peut pas être antérieure à {min_date.strftime('%d/%m/%Y')}.")
    if value > max_date:
        raise ValidationError(f"La date ne peut pas être postérieure à {max_date.strftime('%d/%m/%Y')}.")

def generate_phone():
    first_digit = random.choice([1, 2, 3])
    rest = str(int(time.time() * 1000))
    unique_number = int(str(first_digit) + rest)
    return unique_number
def truncate_gps(coord):
    lat, lon = coord.split(";")
    lat = f"{float(lat):.6f}"
    lon = f"{float(lon):.6f}"
    return f"{lat};{lon}"
def to_slug(phone,coord):
    lat, lon = coord.split(";")
    lat = f"{float(lat):.3f}"
    lon = f"{float(lon):.3f}"
    coord = f"{lat}{lon}"
    res = phone
    txt = coord.replace('.','').replace('-','')
    return slugify(str(phone)+str(txt))

def is_active(entity):
    if entity.contact_phone == "12345678"  or entity.contact_phone.startswith("1"): return False
    t = ("absent","fermer","fermé","fermée","absente")
    if entity.contact_prenom.lower() in t and entity.contact_nom.lower() in t: return False
    return True


def get_status(status):
    if not status: return status
    if status in STATUS_CHOICES_LIST: return [status]
    if status.upper() =="NON_PAYÉ": return STATUS_CHOICES_LIST_NON_PAYE
    if status.upper() == "DEJA_PAYÉ": return STATUS_CHOICES_LIST_PAYE
    return STATUS_CHOICES_LIST


def get_matching_status(status_input):

    status_upper = status_input.upper() if status_input else ""

    if status_upper == "NON_DEMANDÉ":
        return None

    elif status_upper == "NON_PAYÉ":
        return STATUS_CHOICES_LIST_NON_PAYE

    elif status_upper == "DEJA_PAYÉ":
        return STATUS_CHOICES_LIST_PAYE

    elif status_upper in STATUS_CHOICES_LIST:
        return [status_upper]
