import datetime
import uuid

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from diaffrin import settings
from diaffrin_api.models import Commune, Entity


@login_required
def home(request):
    commune = get_object_or_404(Commune, code=request.user.username.lower())
    contexte = {
        "commune": str(commune),
        "entities": commune.entity_set.all()
    }
    return render(request, 'home.html', context=contexte)


@login_required
def carte(request):
    commune = get_object_or_404(Commune, code=request.user.username.lower())
    contexte = {
        "commune": str(commune),
        "entities": commune.entity_set.all()
    }
    return render(request, 'carte.html', context=contexte)


@login_required
def get_entity(request, slug):
    commune = get_object_or_404(Commune, code=request.user.username.lower())
    entity = get_object_or_404(Entity, slug=slug)
    coord = entity.coord
    if coord is None or len(coord) < 5: entity.coord = "10.7879168;-8.204519"
    return render(request, 'detail.html', context={'entity': entity, "commune": str(commune)})


@login_required
def get_paiement(request):
    commune = get_object_or_404(Commune, code=request.user.username.lower())
    today = datetime.date.today()
    clients = []
    year = today.year
    month = today.month
    status = 0
    if request.method == "POST":
        year = int(request.POST.get('year', today.year))
        month = int(request.POST.get('month', today.month))
        status = int(request.POST.get('status', 0))
        if status > 0:
            clients = Entity.objects.filter(paiement__year=year, paiement__month=month).distinct()
        else:
            clients = Entity.objects.exclude(paiement__year=year, paiement__month=month)
    title = "Liste des defauts de paiements : " + str(settings.MONTH[month-1]) + " - " + str(year)
    if status > 0: title = "Liste des paiements :  " + str(settings.MONTH[month-1]) + " - " + str(year)
    context = { 'months' : settings.MONTH,
                'entity': clients,
               'title': title,
               'commune': commune,
               'year': year,
               'month': month,
               'status': status}
    print(list(request.POST.items())) # [('fruits', 'apple'), ('meat', 'beef')]

    return render(request, 'paiement.html', context=context)


@login_required
def insert_data(request):
    df = pd.read_excel("data.xlsx")
    df.fillna('--', inplace=True)

    def insert_row(row):
        try:
            entity = Entity()
            entity.slug = str(uuid.uuid4().hex)
            entity.city = row['ville'].lower()
            entity.locality = row['locality']
            entity.activity = row["activity"]
            entity.property = row["property"]
            entity.contact_name = row["contact_name"]
            entity.contact_phone = row["contact_phone"]
            entity.porte = row["porte"]
            entity.coord = row["coord"]
            entity.status = row["status"]
            entity.commune_id = "ml150202"
            entity.save()

        except Exception as e:
            print(e)

    i = 0
    for index, row in df.iterrows():
        insert_row(row)
        print(i)
        i = i + 1

    return render(request, 'paiement.html')
