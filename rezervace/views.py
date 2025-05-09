from django.shortcuts import render

# Create your views here.
from .models import Location

def location_list(request):
    # Načtení všech lokací z databáze
    locations = Location.objects.all()
    # Předání dat do šablony
    return render(request, 'location_list.html', {'locations': locations})