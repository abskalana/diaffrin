from datetime import  datetime
import uuid
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from diaffrin import settings
from diaffrin_api.forms import MouvementForm
from .constant import *
from diaffrin_api.models import Commune, EntityModel,  Paiement, Mouvement
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from .utils import is_active,  get_matching_status
from .serializer import EntitySerializer


@login_required
def home(request):
    commune = Commune.objects.get(code="150202")
    entities= commune.entitymodel_set.all()

    for i in entities:
        i.save()
    locality = request.GET.get("locality", "")
    status = request.GET.get("status", "")
    property_ = request.GET.get("property", "")
    activity = request.GET.get("activity", "")

    active = request.GET.get("active", "")
    if active != "":
        entities = entities.filter(active=bool(int(active)))


    if locality:
        entities = entities.filter(locality=locality)
    if status:
        entities = entities.filter(status=status)
    if property_:
        entities = entities.filter(property=property_)
    if activity:
        entities = entities.filter(activity=activity)

    context = {
        'commune': commune,
         "entities": entities,
         "localities": LOCALITY_LIST,  # ne contient PAS "Tous"
         "properties": PROPERTY_LIST,  # ne contient PAS "Tous"
         "activities": ACTIVITY_LIST,  # ne contient PAS "Tous"
         "statuses": STATUS_LIST,  # ne contient PAS "Tous"
    }

    return render(request, 'home.html', context=context)


@login_required
def get_entity_paiement(request):
    commune = Commune.objects.get(code="150202")
    auj = datetime.today()
    current_month = MOIS_MAP.get(auj.month)
    annee = request.GET.get("annee", auj.year)
    mois = request.GET.get("mois", current_month)
    city = request.GET.get("city", "")
    locality = request.GET.get("locality", "")
    property_ = request.GET.get("property", "")
    status = request.GET.get("status", "")

    entities= commune.entitymodel_set.all()
    if city:
        entities = entities.filter(city=city)

    if locality:
        entities = entities.filter(locality=locality)

    if property_:
        entities = entities.filter(property=property_)

    serializer = EntitySerializer(entities, many=True, context={"mois": mois, "annee": annee})
    result = []
    if status:
         status_ = get_matching_status(status)
         for i in serializer.data:  # i est un dict
             paiement = i.get("paiement")
             if status_:
                if paiement and paiement.get("status") in status_:
                    result.append(i)
             else:
                 if paiement is None:
                     result.append(i)

    else:
        result = serializer.data

    nombre_items = len(result)
    nombre_portes = sum(e.get("porte") for e in result)
    montant_total = sum(e.get("paiement").get("value",0) for e in result if e.get("paiement"))


    context = {
        'commune': commune,
         "entities": result,
        'nombre_items': nombre_items,
        'nombre_portes': nombre_portes,
        'montant_total': montant_total,
         "city": PLACES,
         "localities": LOCALITY_LISTS + [p for p in PLACES if p != "Kalana"],  # ne contient PAS "Tous"
         "properties": PROPERTY_LIST,  # ne contient PAS "Tous"
         "activities": ACTIVITY_LIST,  # ne contient PAS "Tous"
         "statuses": STATUS_CHOICES_LIST_ALL,  # ne contient PAS "Tous"
         "year_selected": annee,
         "current_year": auj.year,
         "MONTH_CHOICES": MONTH_CHOICES,
         "mois_selected": mois,
    }

    return render(request, 'entity_paiement.html', context=context)

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
    today = datetime.today()
    current_month = MOIS_MAP.get(today.month)
    mois = request.GET.get("mois",current_month)
    sens = request.GET.get("sens")
    nature = request.GET.get("nature")
    source = request.GET.get("source")
    category = request.GET.get("category")
    annee = request.GET.get("annee", today.year)
    download = request.GET.get("download")
    commune = Commune.objects.get(code="150202")

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
        'commune': commune,
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

    if download == "excel":
        df = pd.DataFrame.from_records(mouvements.values())
        for col in df.select_dtypes(include=["datetimetz"]).columns:
            df[col] = df[col].dt.tz_localize(None)
        today_str = datetime.today().strftime("%Y-%m-%d")
        filename = f"mouvements_{today_str}.xlsx"
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        df.to_excel(response, index=False)
        return response

    return render(request, "mouvement_list.html", context)
@login_required
def create_mouvement(request):
    commune = Commune.objects.get(code="150202")
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

    return render(request, "mouvement_add.html", {"form": form, "success_message": success_message,'commune': commune})

@login_required
def entity_paiements(request):
    annee = request.GET.get('annee')
    mois = request.GET.get('mois')
    status = request.GET.get('status',"")
    ticket = request.GET.get('ticket')
    download = request.GET.get("download")
    commune = Commune.objects.get(code="150202")
    paiements = Paiement.objects.select_related("entity_model").order_by("-date_created")

    if annee and annee.isdigit():
        paiements = paiements.filter(annee=int(annee))
    if mois:
        paiements = paiements.filter(mois=mois)
    if status:
        paiements = paiements.filter(status=status)

    if ticket:
       paiements = paiements.filter(ticket_type=ticket)

    context = {
        'commune': commune,
        "paiements": paiements,
        "annee": annee or "",
        "mois": mois or "",
        "status": status or "",
        "MONTH_CHOICES": MONTH_CHOICES,
        "STATUS_CHOICES": STATUS_CHOICES,
        "TYPE_TICKET": TYPE_TICKET ,
    }

    if download == "excel":
        df = pd.DataFrame.from_records(paiements.values())
        for col in df.select_dtypes(include=["datetimetz"]).columns:
            df[col] = df[col].dt.tz_localize(None)
        today_str = datetime.today().strftime("%Y-%m-%d")
        filename = f"paiements_{today_str}.xlsx"
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        df.to_excel(response, index=False)
        return response

    return render(request, "paiement.html", context)

@login_required
def entity_detail_view(request, pk):
    # Récupère l'entité par son UUID
    entity = get_object_or_404(EntityModel, pk=pk)


    payments = Paiement.objects.filter(entity_model=entity).order_by('-date_created')

    commune = Commune.objects.get(code="150202")
    context = {
        'commune': commune,
        'entity': entity,
        'payments': payments,
    }
    return render(request, 'detail.html', context)
