from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from diaffrin_api.models import Commune


@login_required
def home(request):
    commune = get_object_or_404(Commune, pk= request.user.username)
    contexte ={
        "commune" : str(commune),
        "entities": [0,1,2,3,4,5,6,7,8,9]
    }
    return render(request, 'home.html', context=contexte)
