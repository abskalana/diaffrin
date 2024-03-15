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
    entity = get_object_or_404(Entity, slug= slug)
    return render(request, 'detail.html', context={'entity': entity})


@login_required
def get_paiement(request):
    today = datetime.date.today()
    year = request.POST.get('year', today.year)
    month = request.POST.get('month', today.month)
    clients_pai = Entity.objects.filter(paiement__year=year, paiement__month=month).distinct()
    clients_without_payments = Entity.objects.exclude(paiement__year=year, paiement__month=month)
    context = {'client_pay': clients_pai,
               'year': year,
               'month': month,
               'client_not_pay': clients_without_payments}
    return render(request, 'paiement.html', context={'client_pay': clients_pai, 'client_not_pay': clients_without_payments})
