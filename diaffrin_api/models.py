from django.db import models

class Commune(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    tel_fixe = models.CharField(max_length=30)
    tel_mobile_1 = models.CharField(max_length=30)
    tel_mobile_2 = models.CharField(max_length=30)
    chef_lieu = models.CharField(max_length=30)

class Entity(models.Model):
    id = models.AutoField(primary_key=True)
    ville = models.CharField(max_length=30)
    quartier = models.CharField(max_length=30)
    category = models.CharField(max_length=50)
    speciality = models.CharField(max_length=100)
    nom = models.CharField(max_length=50)
    horaire = models.CharField(max_length=50, default="08h-20h")
    property = models.CharField(max_length=30, default="LOCATAIRE")
    nom_complet = models.CharField(max_length=30, default="Inconnu")
    telephone = models.CharField(max_length=30, default="0000000")
    nbr_porte = models.IntegerField(default=1)
    coords = models.CharField(max_length=100, default="0.00;0.00")
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)