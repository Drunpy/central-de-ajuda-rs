from django.shortcuts import render
from .models import Abrigos

def mapa_de_abrigos_view(request):
    abrigos = Abrigos.objects.all()
    return render(
        request,
        'mapa_de_abrigos.html',
        {
            'abrigos': abrigos
        }
    )
