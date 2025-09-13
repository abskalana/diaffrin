import datetime
import uuid

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from diaffrin import settings
from diaffrin_api.forms import MouvementForm
from diaffrin_api.models import Commune, Entity,Personnel,Mouvement,MONTH_CHOICES,SENS_CHOICES,NATURE_CHOICES,SOURCE_CHOICES
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404


@login_required
def home(request):
    commune = get_object_or_404(Commune, code="150202")
    contexte = {
        "commune": str(commune),
        "entities": commune.entity_set.all()
    }
    return render(request, 'home.html', context=contexte)

@csrf_exempt
def login_view(request):
    username = ""
    password = ""
    if request.method == "GET":
         username = request.GET.get("username")
         password = request.GET.get("password")
    else:
         username = request.POST.get("username")
         password = request.POST.get("password")
    employer = get_object_or_404(Personnel, id=username)
    if employer.password == password:
          return HttpResponse("true", content_type="text/plain")
    return  HttpResponse("false", content_type="text/plain")



@login_required
def mouvement_list(request):
    mouvements = Mouvement.objects.all().order_by("-date")
    mois = request.GET.get("mois")
    sens = request.GET.get("sens")
    nature = request.GET.get("nature")
    source = request.GET.get("source")

    if mois:
        mouvements = mouvements.filter(mois=mois)
    if sens:
        mouvements = mouvements.filter(sens=sens)
    if nature:
        mouvements = mouvements.filter(nature=nature)
    if source:
        mouvements = mouvements.filter(source=source)

    # transmettre aussi les valeurs actuelles pour préremplir le formulaire
    somme_total = mouvements.aggregate(Sum("total"))["total__sum"] or 0

    context = {
        "mouvements": mouvements,
        "mois_selected": mois,
        "sens_selected": sens,
        "nature_selected": nature,
        "source_selected": source,
        "MONTH_CHOICES":MONTH_CHOICES,
        "SENS_CHOICES": SENS_CHOICES,
        "NATURE_CHOICES": NATURE_CHOICES,
        "SOURCE_CHOICES": SOURCE_CHOICES,
        'total':somme_total,
    }
    return render(request, "mouvement_list.html", context)
@login_required
def create_mouvement(request):
    success_message = None

    if request.method == "POST":
        form = MouvementForm(request.POST)
        if form.is_valid():
            mouvement = form.save(commit=False)
            mouvement.user = request.user
            mouvement.save()
            success_message = "Operations enregistré avec succès !"
            form = MouvementForm()  # reset le formulaire
    else:
        form = MouvementForm()

    return render(request, "mouvement_add.html", {"form": form, "success_message": success_message})
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
