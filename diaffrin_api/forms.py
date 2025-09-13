import datetime
import uuid


from django import forms
from .models import Mouvement

class MouvementForm(forms.ModelForm):
    class Meta:
        model = Mouvement
        fields = [
            "date", "mois", "annee", "city", "sens", "name", "nature",
            "source", "beneficiaire", "quantite", "montant","commentaire"
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "mois": forms.Select(attrs={"class": "form-control"}),
            "annee": forms.NumberInput(attrs={"class": "form-control"}),
            "city": forms.Select(attrs={"class": "form-control"}),
            "sens": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "nature": forms.Select(attrs={"class": "form-control"}),
            "source": forms.Select(attrs={"class": "form-control"}),
            "beneficiaire": forms.Select(attrs={"class": "form-control"}),
            "quantite": forms.NumberInput(attrs={"class": "form-control"}),
            "montant": forms.NumberInput(attrs={"class": "form-control"}),
            "commentaire": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }




