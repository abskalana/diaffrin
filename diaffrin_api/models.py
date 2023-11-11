from django.db import models


class Commune(models.Model):
    id = models.CharField(primary_key=True,max_length=10)
    name = models.CharField(max_length=50)
    region = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    tel_fixe = models.CharField(max_length=30)
    tel_mobile_1 = models.CharField(max_length=30)
    tel_mobile_2 = models.CharField(max_length=30)
    chef_lieu = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + " - " + self.name

    def __repr__(self):
        return str(self.id) + " - " + self.name


class Entity(models.Model):
    id = models.AutoField(primary_key=True)
    ville = models.CharField(max_length=30)
    quartier = models.CharField(max_length=30, default="No", blank=True, null=True)
    category = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100, default="No",blank=True, null=True)
    nom = models.CharField(max_length=50, default="",blank=True, null=True)
    horaire = models.CharField(max_length=50, default="08h-20h")
    property = models.CharField(max_length=30, default="PRIVEE")
    nom_complet = models.CharField(max_length=30, default="No",blank=True, null=True)
    telephone = models.CharField(max_length=30, default="-1",blank=True, null=True)
    nbr_porte = models.IntegerField(default=1)
    coords = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

class Paiement(models.Model):
    id = models.AutoField(primary_key=True)
    id_device = models.CharField(max_length=50)
    year = models.IntegerField(default=-1)
    month = models.CharField(max_length=20)
    montant = models.IntegerField(default=0)
    date_reference = models.DateTimeField(auto_now_add=True)
    date_paiement = models.DateTimeField(auto_now_add=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    coords = models.CharField(max_length=100)
