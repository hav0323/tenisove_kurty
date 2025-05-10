from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm


# Create your views here.
from .models import Location

def location_list(request):
    # Načtení všech lokací z databáze
    locations = Location.objects.all()
    # Předání dat do šablony
    return render(request, 'rezervace/location_list.html', {'locations': locations})

@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # Přiřadíme aktuálního uživatele
            reservation.save()
            return redirect('reservation_list')  # Přesměrování na seznam rezervací
    else:
        form = ReservationForm()
    return render(request, 'rezervace/reservation_form.html', {'form': form})

def homepage(request):
    form = ReservationForm()
    return render(request, 'rezervace/homepage.html', {'form': form})