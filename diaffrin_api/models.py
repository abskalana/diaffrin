from django.db import models
from django.urls import reverse
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from .utils import validate_date_range

MOIS_MAP = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre",
}
PLACE_CHOICES = [
        ("KALANA", "Kalana"),
        ("NIESSOUMALA", "Niessoumala"),
        ("TRAORELA", "Traorela"),
        ("DIABALA", "Diabala"),
        ("BALANTOUMOU", "Balantoumou"),
        ("FABOULA", "Faboula"),
        ("KALAKO", "Kalako"),
        ("LADJIKOUROULA", "Ladjikouroula"),
        ("SOLOMANINA", "Solomanina"),
        ("SADIOUROULA", "Sadiouroula"),
        ("DAOLILA", "Daolila"),
        ("DADJOUGOUBALA", "Dadjougoubala"),
        ("BADA", "Bada"),
        ("BANDIALA", "Bandiala"),
        ("BEREBOGOLA", "Bèrèbogola"),
        ("DABARAN", "Dabaran"),
        ("DALAGUE", "Dalaguè"),
        ("DANGOUe", "Dangouè"),
        ("DIANSIRALA", "Diansirala"),
        ("HADJILA", "Hadjila"),
        ("HADJILAMININA", "Hadjilaminina"),
        ("KONFRA", "Konfra"),
        ("KOSSIALA", "Kossiala"),
        ("KOUMBALA", "Koumbala"),
        ("LEBA", "Lèba"),
        ("MANDEBALA", "Mandebala"),
        ("NENEDIANA", "Nènèdiana"),
        ("NOUNFRA", "Nounfra"),
        ("SALALA", "Salala"),
        ("SAMERILA", "Samerila"),
        ("SOKOROKO", "SôkôrôKô"),
    ]

MONTH_CHOICES = [
        ("Janvier", "Janvier"),
        ("Février", "Février"),
        ("Mars", "Mars"),
        ("Avril", "Avril"),
        ("Mai", "Mai"),
        ("Juin", "Juin"),
        ("Juillet", "Juillet"),
        ("Août", "Août"),
        ("Septembre", "Septembre"),
        ("Octobre", "Octobre"),
        ("Novembre", "Novembre"),
        ("Décembre", "Décembre"),
    ]


SENS_CHOICES = [
        ("entree", "entree"),
        ("sortie", "sortie"),
    ]

TYPE_CHOICES = [
        ("Activité", "Activité"),
        ("Reserve", "Reserve"),
        ("Caisse", "Caisse"),
    ]

SOURCE_CHOICES = [
        ("Marché", "Marché"),
        ("Commerce", "Commerce"),
        ("Espace", "Espace public"),
        ("Tous", "Tous"),
    ]


NATURE_CHOICES = [
        ("salaire", "salaire"),
        ("recette", "recette"),
        ("depense", "depense"),
        ("achat", "achat materiel"),
         ("budget", "budget"),
        ("propriété", "propriété"),
    ]

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



    def get_absolute_url(self):
        return reverse("entity_detail", kwargs={"slug": self.id})

    def get_display_name(self):
        return self.activity + " - "+ self.contact_name



class Mouvement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=timezone.now,validators=[validate_date_range])
    mois = models.CharField(max_length=50, choices=MONTH_CHOICES)
    annee = models.IntegerField(
        validators=[
            MinValueValidator(2024),
            MaxValueValidator(datetime.date.today().year + 20)
        ],
        default=datetime.date.today().year)
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

    def save(self, *args, **kwargs):
        if self.sens.lower() == "sortie" :
             self.montant = -abs(self.montant)
        elif self.sens.lower() == "entree" :
             self.montant = abs(self.montant)
        self.total = self.montant*self.quantite
        self.annee = self.date.year
        self.mois = MOIS_MAP[self.date.month]
        super().save(*args, **kwargs)