from django.db import models
from django.urls import reverse
import uuid


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


class Entity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.CharField(unique=True, max_length=30)
    city = models.CharField(max_length=30)
    locality = models.CharField(max_length=50, blank=True, null=True)
    activity = models.CharField(max_length=100, blank=True, null=True)
    property = models.CharField(max_length=30, default="PRIVEE")
    type_property = models.CharField(max_length=30, default="MAISON")
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_prename = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=30, blank=True, null=True)
    entity_name = models.CharField(max_length=50, blank=True, null=True)
    entity_phone = models.CharField(max_length=50, blank=True, null=True)
    porte = models.IntegerField(default=1)
    montant = models.IntegerField(default=1)
    coord = models.CharField(max_length=100)
    paiement_status = models.CharField(max_length=20)
    status = models.CharField(max_length=20,default="OUVERT")
    meta_user = models.CharField(max_length=20, default="user")
    meta_created = models.DateTimeField(auto_now_add=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("entity_detail", kwargs={"slug": self.slug})

    def get_display_name(self):
        return self.activity + " - "+ self.contact_name
