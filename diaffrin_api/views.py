import datetime
import uuid

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from diaffrin import settings
from diaffrin_api.models import Commune, Entity,Personnel


@login_required
def home(request):
    commune = get_object_or_404(Commune, code=request.user.username.lower())
    contexte = {
        "commune": str(commune),
        "entities": commune.entity_set.all()
    }
    return render(request, 'home.html', context=contexte)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            username = data.get("username")
            password = data.get("password")
            employer = Personnel.objects.get(code=username, password=password, status=0)
            return JsonResponse({"status": 0})


        except Exception as e:
            return JsonResponse({"status": -1})
    return JsonResponse({"status": -1})


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
    title = "Liste des paiements :  " + str(settings.MONTH[month - 1]) + " - " + str(year)
    status = 0
    if request.method == "POST":
        year = int(request.POST.get('year', today.year))
        month = int(request.POST.get('month', today.month))
        status = int(request.POST.get('status', 0))
        if status > 0:
            clients = Entity.objects.filter(paiement__year=year, paiement__month=month)
            title = "Liste des paiements :  " + str(settings.MONTH[month - 1]) + " - " + str(year)
        else:
            clients = Entity.objects.exclude(paiement__year=year, paiement__month=month)
            title = "Liste des defauts de paiements : " + str(settings.MONTH[month - 1]) + " - " + str(year)
    context = { 'months' : settings.MONTH,
                'entity': clients,
               'title': title,
               'commune': commune,
               'year': year,
               'month': month,
               'status': status}
    return render(request, 'paiement.html', context=context)
