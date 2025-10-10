from django.db import models
from django.urls import reverse
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from .utils import validate_date_range, is_active, truncate_gps, to_slug, generate_phone
from django.utils.text import slugify
from .constant import *
import time

class Commune(models.Model):
    id = models.CharField(primary_key=True, max_length=12)
    code = models.CharField(unique=True, max_length=12)
    name = models.CharField(max_length=50)
    coord = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=50)

    def __str__(self):
        return str(self.code).upper() + " - " + self.name

    def __repr__(self):
        return str(self.code).upper() + " - " + self.name


class EntityModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=30,default="Kalana")
    locality = models.CharField(max_length=50, blank=True, null=True)
    activity = models.CharField(max_length=50, blank=True, null=True)
    property = models.CharField(max_length=30, default="PRIVEE")
    type_entity = models.CharField(max_length=30, default="MAISON")
    contact_nom = models.CharField(max_length=30, blank=True, null=True)
    contact_prenom = models.CharField(max_length=30, blank=True, null=True)
    contact_phone = models.CharField(max_length=30, blank=True, null=True)
    porte = models.IntegerField(default=1)
    coord = models.CharField(max_length=100,default="OUVERT")
    status = models.CharField(max_length=20,default="OUVERT")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE,default="150202")
    active = models.BooleanField(default=True)
    numero = models.IntegerField(default=1)
    nif = models.CharField(max_length=30, blank=True, null=True)
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['-date_created']
        unique_together = ('numero', 'contact_phone')

    def save(self, *args, **kwargs):
        self.active = is_active(self)
        if not self.active: self.contact_phone = generate_phone()
        self.coord = truncate_gps(self.coord)
        self.slug = to_slug(self.contact_phone,self.coord)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("entity-detail", kwargs={"pk": str(self.id)})


    def get_display_name(self):
        prenom = self.contact_prenom or ""
        nom = (self.contact_nom or "").upper()  # nom en majuscule
        phone = self.contact_phone or ""

        contact_parts = [part for part in [prenom, nom] if part]
        contact_str = " ".join(contact_parts)

        if contact_str and phone:
            return f"{contact_str} - {phone}"
        elif contact_str:
            return contact_str
        elif phone:
            return phone
        else:
            return "---"

    def get_paiement(self, mois=None, annee=None):
        now = timezone.now()
        if annee is None: annee = now.year
        if mois is None : mois = MOIS_MAP[now.month]

        try:
            return Paiement.objects.get(entity_model=self, annee=annee, mois=mois)
        except :
            return None

    def get_impot(self, annee=None):
        now = timezone.now()
        if annee is None: annee = now.year
        try:
            return Impot.objects.get(entity_model=self, annee=annee)
        except:
            return None


class Mouvement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=timezone.now,validators=[validate_date_range])
    mois = models.CharField(max_length=50, choices=MONTH_CHOICES)
    annee = models.IntegerField(
        validators=[
            MinValueValidator(2024),
            MaxValueValidator(datetime.today().year + 20)
        ],
        default=datetime.today().year)
    city = models.CharField(max_length=50, choices=PLACE_CHOICES,default="KALANA")
    sens = models.CharField(max_length=50, choices=SENS_CHOICES)
    name = models.CharField(max_length=100)
    nature =  models.CharField(max_length=50, choices=NATURE_CHOICES)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    category = models.CharField(max_length=20, choices=TYPE_CHOICES,default="Activité")
    beneficiaire = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    quantite = models.IntegerField(default=1,validators=[MinValueValidator(1)])
    montant = models.IntegerField(validators=[MinValueValidator(99)])
    total = models.IntegerField(default=1)
    description =  models.CharField(max_length=200, blank=True, null=True)
    commentaire =  models.CharField(max_length=200, blank=True, null=True,default="")
    date_created = models.DateTimeField(default=timezone.now)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE,default="150202")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        if self.sens.lower() == "sortie" :
             self.montant = -abs(self.montant)
        elif self.sens.lower() == "entree" :
             self.montant = abs(self.montant)
        self.total = self.montant*self.quantite
        self.annee = self.date.year
        self.mois = MOIS_MAP[self.date.month]
        super().save(*args, **kwargs)




class Paiement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.IntegerField(default=0)
    ticket_type = models.CharField(max_length=20, choices=TYPE_TICKET,default="")
    annee = models.IntegerField(default=datetime.today().year)
    period = models.CharField(max_length=50, choices=MONTH_CHOICES, default="Septembre")
    mois = models.CharField(max_length=50, choices=MONTH_CHOICES,default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    entity_model = models.ForeignKey(EntityModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coord = models.CharField(max_length=30)
    commentaire =  models.CharField(max_length=200, blank=True, null=True,default="")
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']
        unique_together = ('entity_model', 'annee', 'mois', 'value','status')


class Impot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.IntegerField(default=0)
    annee = models.IntegerField(default=datetime.today().year)
    centre = models.CharField(max_length=50, choices=CENTRE_IMPOT, default="YANFOLILA")
    status = models.CharField(max_length=20, choices=STATUS_IMPOT)
    entity_model = models.ForeignKey(EntityModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coord = models.CharField(max_length=30)
    commentaire =  models.CharField(max_length=100, blank=True, null=True,default="")
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']
        unique_together = ('entity_model', 'annee')


