from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ReservationForm
from .models import Location, Court

# Create your views here.

def location_list(request):
    # Načtení všech lokací z databáze
    locations = Location.objects.all()
    # Předání dat do šablony
    return render(request, 'rezervace/location_list.html', {'locations': locations})

def location_detail(request, pk):
    # Načtení konkrétní lokace podle primárního klíče (pk)
    location = get_object_or_404(Location, pk=pk)
    return render(request, 'rezervace/location_detail.html', {'location': location})

def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'rezervace/reservation_form.html', {'form': form})

def homepage(request):
    form = ReservationForm()
    return render(request, 'rezervace/homepage.html', {'form': form})

def ajax_load_courts(request):
    location_id = request.GET.get('location')  # Získání ID lokace z požadavku
    courts = Court.objects.filter(location_id=location_id)  # Filtrování kurtů podle lokace
    return render(request, 'rezervace/court_dropdown_list_options.html', {'courts': courts})

