import uuid

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from diaffrin_api.models import Commune, Entity
import datetime

@login_required
def home(request):
    commune = get_object_or_404(Commune, code= request.user.username)
    contexte ={
        "commune" : str(commune),
        "entities": commune.entity_set.all()
    }
    return render(request, 'home.html', context=contexte)

@login_required
def get_entity(request, slug):
    commune = get_object_or_404(Commune, code=request.user.username)
    entity = get_object_or_404(Entity, slug= slug)
    return render(request, 'detail.html', context={'entity': entity, "commune" : str(commune)})


@login_required
def get_paiement(request):
    commune = get_object_or_404(Commune, code=request.user.username)
    today = datetime.date.today()
    year = request.POST.get('year', today.year)
    month = request.POST.get('month', today.month)
    status = request.POST.get('month', today.month)
    clients = Entity.objects.filter(paiement__year=year, paiement__month=month).distinct()
    context = {'client_pay': clients,
               'commune': commune,
               'year': year,
               'month': month,
               'client_not_pay': clients}
    return render(request, 'paiement.html', context=context)

@login_required
def insert_data(request ):
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