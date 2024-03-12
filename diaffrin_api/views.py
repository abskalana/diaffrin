from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from diaffrin_api.models import Commune

@login_required
def home(request):
    commune = get_object_or_404(Commune, pk= request.user.username)
    contexte ={
        "commune" : str(commune),
        "entities": commune.entity_set.all()
    }
    return render(request, 'home.html', context=contexte)