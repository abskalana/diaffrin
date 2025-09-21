from django.db import models
from django.urls import reverse
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from .utils import validate_date_range, to_slug, truncate_gps
from django.utils.text import slugify


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


STATUS_CHOICES = [
        ("PAYÉ", "PAYÉ"),
        ("REFUS", "REFUS"),
        ("FERMÉ", "FERMÉ"),
        ("ABSENT", "ABSENT"),
        ("PAYE_MAIRIE", "PAYE_MAIRIE"),
        ("AUTRE", "AUTRE"),
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


TYPE_TICKET = [
        ("TK100", "TK100"),
        ("TK1000", "TK1000"),
        ("TK5000", "TK5000"),
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


class EntityModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=30)
    locality = models.CharField(max_length=50, blank=True, null=True)
    activity = models.CharField(max_length=50, blank=True, null=True)
    property = models.CharField(max_length=30, default="PRIVEE")
    type_entity = models.CharField(max_length=30, default="MAISON")
    contact_nom = models.CharField(max_length=30, blank=True, null=True)
    contact_prenom = models.CharField(max_length=30, blank=True, null=True)
    contact_phone = models.CharField(max_length=30, blank=True, null=True)
    porte = models.IntegerField(default=1)
    coord = models.CharField(max_length=100)
    status = models.CharField(max_length=20,default="OUVERT")
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE,default="150202")

    def save(self, *args, **kwargs):
        self.coord = truncate_gps(self.coord)
        self.slug = slugify(to_slug(self.contact_phone, self.coord))
        super().save(*args, **kwargs)



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




class Paiement(models.Model):
    uuid = models.CharField(unique=True, max_length=120)
    value = models.IntegerField(default=0)
    ticket_num = models.IntegerField(default=0)
    ticket_type = models.CharField(max_length=20, choices=TYPE_TICKET)
    annee = models.IntegerField(default=0)
    mois = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    entity_model = models.ForeignKey(EntityModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coord = models.CharField(max_length=100)
    commentaire =  models.CharField(max_length=200, blank=True, null=True,default="")
    date_created = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        self.annee = self.date.year
        self.mois = MOIS_MAP[self.date.month]
        super().save(*args, **kwargs)

