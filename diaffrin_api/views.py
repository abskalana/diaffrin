import datetime
import uuid

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from diaffrin import settings
from diaffrin_api.forms import MouvementForm
from diaffrin_api.models import Commune, EntityModel,  TYPE_CHOICES, Mouvement, MONTH_CHOICES, SENS_CHOICES, \
    NATURE_CHOICES, SOURCE_CHOICES, MOIS_MAP
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404
import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


@login_required
def home(request):
    commune = Commune.objects.get(code="150202")
    context = {
        "commune": str(commune),
        "entities": commune.entitymodel_set.all()
    }
    return render(request, 'home.html', context=context)

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

    user = authenticate(request, username=username, password=password)
    if user is not None:
        return HttpResponse(user.id, content_type="text/plain")
    else:
        return HttpResponse("false", content_type="text/plain")


@login_required
def mouvement_list(request):
    mouvements = Mouvement.objects.all().order_by("-date_created", "-date")
    today = datetime.date.today()
    current_month = MOIS_MAP.get(today.month)
    mois = request.GET.get("mois",current_month)
    sens = request.GET.get("sens")
    nature = request.GET.get("nature")
    source = request.GET.get("source")
    category = request.GET.get("category")
    annee = request.GET.get("annee", today.year)

    if annee:
        mouvements = mouvements.filter(annee=annee)
    if mois:
        mouvements = mouvements.filter(mois=mois)
    if sens:
        mouvements = mouvements.filter(sens=sens)
    if nature:
        mouvements = mouvements.filter(nature=nature)
    if source:
        mouvements = mouvements.filter(source=source)

    if category:
        mouvements = mouvements.filter(category=category)



    # transmettre aussi les valeurs actuelles pour préremplir le formulaire
    somme_total = sum(m.total for m in mouvements if m.category  == "Activité")
    somme_reserve = sum(m.total for m in mouvements if m.category  == "Reserve")
    somme_caisse = sum(m.total for m in mouvements if m.category  == "Caisse")

    context = {
        "mouvements": mouvements,
        "mois_selected": mois,
        "sens_selected": sens,
        "nature_selected": nature,
        "source_selected": source,
        "year_selected": annee,
        "current_year": today.year,
        "MONTH_CHOICES":MONTH_CHOICES,
        "SENS_CHOICES": SENS_CHOICES,
        "NATURE_CHOICES": NATURE_CHOICES,
        "SOURCE_CHOICES": SOURCE_CHOICES,
        "TYPE_CHOICES": TYPE_CHOICES,
        'somme_total':somme_total,
        'somme_reserve': somme_reserve,
        'somme_caisse': somme_caisse,
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
    entity = get_object_or_404(EntityModel, slug=slug)
    coord = entity.coord
    if coord is None or len(coord) < 5: entity.coord = "10.7879168;-8.204519"
    return render(request, 'detail.html', context={'entity': entity, "commune": str(commune)})


@login_required
def get_paiement(request):
    return render(request, 'paiement.html', context=context)
