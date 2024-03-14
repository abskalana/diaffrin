from django.db import models


class Commune(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)
    coord = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=50)

    def __str__(self):
        return str(self.code) + " - " + self.name

    def __repr__(self):
        return str(self.code) + " - " + self.name


class Entity(models.Model):
    slug = models.CharField(unique=True,max_length=120)
    city = models.CharField(max_length=30)
    locality = models.CharField(max_length=50, blank=True, null=True)
    activity = models.CharField(max_length=100, blank=True, null=True)
    property = models.CharField(max_length=30, default="PRIVEE")
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=30, blank=True, null=True)
    porte = models.IntegerField(default=1)
    coord = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    def get_display_name(self):
        if len(self.name) > 0 : return  self.name
        return "Entité de "+ self.contact_last_name + " " + self.contact_first_name


class Paiement(models.Model):
    uuid = models.CharField(unique=True,max_length=120)
    value = models.IntegerField(default=0)
    annee = models.IntegerField(default=2024)
    mois = models.CharField(max_length=20)
    date_pai = models.DateTimeField(auto_now_add=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    coord = models.CharField(max_length=100)

    class Meta:
        ordering = ["annee","mois"]
