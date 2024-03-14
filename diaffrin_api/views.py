from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from diaffrin_api.models import Commune, Entity


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
