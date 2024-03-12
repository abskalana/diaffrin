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
    city = models.CharField(max_length=30)
    locality = models.CharField(max_length=50, default="No", blank=True, null=True)
    category = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100, default="No", blank=True, null=True)
    name = models.CharField(max_length=100, default="", blank=True, null=True)
    property = models.CharField(max_length=30, default="PRIVEE")
    contact_last_name = models.CharField(max_length=100, default="No", blank=True, null=True)
    contact_first_name = models.CharField(max_length=100, default="No", blank=True, null=True)
    contact_phone = models.CharField(max_length=30, default="-1", blank=True, null=True)
    porte = models.IntegerField(default=1)
    coord = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)


class Paiement(models.Model):
    uuid = models.CharField(max_length=50)
    value = models.IntegerField(default=0)
    date_ref = models.DateTimeField(auto_now_add=True)
    date_pai = models.DateTimeField(auto_now_add=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    agent = models.ForeignKey(Entity, on_delete=models.CASCADE)
    coord = models.CharField(max_length=100)
