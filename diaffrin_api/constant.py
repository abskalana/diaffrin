PROPERTY_LIST = [
    "PRIVEE",
    "ESPACE PUBLIC",
    "MARCHE",
]

ACTIVITY_LIST = [
    "Boutique divers",
    "Boutique spécialisée",
    "Autres commerces",
    "Autres services",
    "Alimentation",
    "Boucherie",
    "Boulangerie",
    "Coiffure",
    "Couture",
    "Electronique",
    "Formation",
    "Garage Moto",
    "Garage Auto",
    "Garage Pneu",
    "Grabale",
    "Poissonnerie",
    "Volaille",
    "Industrie bois",
    "Industrie metallique",
    "Lavage",
    "Loisir",
    "Magasin de depots",
    "Magasin fermée",
    "Moulin",
    "Or",
    "Quincaillerie",
    "Rebobinage",
    "Restauration",
    "Santé",
    "Service reparation",
    "Table Fruits",
    "Table condiments",
    "Transfert financier",
    "Media",
    "Katakatani",
    "Moto Taxi",
    "Transport",
    "Textile",
    "Technologie",
    "Restaurant",
    "Boisson",
]

# choices.py (recommended)
LOCALITY_LIST = [
    "Kalana Centre",
    "Kalana Koko",
    "Kalana Kelibougou",
    "Kalana Camp coroni",
    "Kalana Camp",
    "Kalana Dabaranbougou",
    "Kalana",
]

PROPERTY_LIST = [
    "PRIVEE",
    "ESPACE PUBLIC",
    "MARCHE",
]

ACTIVITY_LIST = [
    "Boutique divers",
    "Boutique spécialisée",
    "Autres commerces",
    "Autres services",
    "Alimentation",
    "Boucherie",
    "Boulangerie",
    "Coiffure",
    "Couture",
    "Electronique",
    "Formation",
    "Garage Moto",
    "Garage Auto",
    "Garage Pneu",
    "Grabale",
    "Poissonnerie",
    "Volaille",
    "Industrie bois",
    "Industrie metallique",
    "Lavage",
    "Loisir",
    "Magasin de depots",
    "Magasin fermée",
    "Moulin",
    "Or",
    "Quincaillerie",
    "Rebobinage",
    "Restauration",
    "Santé",
    "Service reparation",
    "Table Fruits",
    "Table condiments",
    "Transfert financier",
    "Media",
    "Katakatani",
    "Moto Taxi",
    "Transport",
    "Textile",
    "Technologie",
    "Restaurant",
    "Boisson",
]

STATUS_LIST = [
    "OUVERT",
    "ABSENT",
    "FERME",
]
STATUS_CHOICES_LIST = [
    "PAYÉ",
    "REFUS",
    "FERMÉ",
    "ABSENT",
    "PAYE_MAIRIE",
    "AUTRE"
]

STATUS_CHOICES_LIST_NON_PAYE = [
    "REFUS",
    "FERMÉ",
    "ABSENT",
    "AUTRE"
]

STATUS_CHOICES_LIST_ALL = ["DEJA_PAYÉ","NON_PAYÉ",'NON_DEMANDÉ']+STATUS_CHOICES_LIST

STATUS_CHOICES_LIST_PAYE = [
    "PAYÉ",
    "PAYE_MAIRIE",
 ]


LOCALITY_LISTS = [
    'Kalana',
    "Kalana Centre",
    "Kalana Koko",
    "Kalana Kelibougou",
    "Kalana Camp coroni",
    "Kalana Camp",
    "Kalana Dabaranbougou",
]

PLACES = [
    "Kalana",
    "Niessoumala",
    "Traorela",
    "Diabala",
    "Balantoumou",
    "Faboula",
    "Kalako",
    "Ladjikouroula",
    "Solomanina",
    "Sadiouroula",
    "Daolila",
    "Dadjougoubala",
    "Bada",
    "Bandiala",
    "Bèrèbogola",
    "Dabaran",
    "Dalaguè",
    "Dangouè",
    "Diansirala",
    "Hadjila",
    "Hadjilaminina",
    "Konfra",
    "Kossiala",
    "Koumbala",
    "Lèba",
    "Mandebala",
    "Nènèdiana",
    "Nounfra",
    "Salala",
    "Samerila",
    "SôkôrôKô",
]


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