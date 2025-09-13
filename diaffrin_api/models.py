from django.db import models
from django.urls import reverse
import uuid
from django.utils import timezone
from django.contrib.auth.models import User


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

class Personnel(models.Model):
    id = models.CharField(primary_key=True, max_length=12)
    name = models.CharField(max_length=50)
    prenom = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Entity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    paiement_status = models.CharField(max_length=20,default="PAYEE")
    status = models.CharField(max_length=20,default="OUVERT")
    meta_user = models.CharField(max_length=20, default="user")
    meta_created = models.DateTimeField(default=timezone.now)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(str(self.contact_phone) + str(self.entity_phone))
            slug_candidate = base_slug
            num = 1
            while Entity.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{num}"
                num += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("entity_detail", kwargs={"slug": self.slug})

    def get_display_name(self):
        return self.activity + " - "+ self.contact_name
