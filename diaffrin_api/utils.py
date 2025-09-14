import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

def validate_date_range(value):
    today = timezone.now().date()
    min_date = today - datetime.timedelta(days=10)
    max_date = today + datetime.timedelta(days=10)

    if value < min_date:
        raise ValidationError(f"La date ne peut pas être antérieure à {min_date.strftime('%d/%m/%Y')}.")
    if value > max_date:
        raise ValidationError(f"La date ne peut pas être postérieure à {max_date.strftime('%d/%m/%Y')}.")