import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify

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
    coord = f"{lat};{lon}"
    res = phone.replace(',','')
    txt = coord.replace(';','')
    return slugify(res+"-"+txt)
