from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ReservationForm, ReviewForm, TournamentRegistrationForm 
from .models import Location, Court, Reservation, Tournament

# Create your views here.

def location_list(request):
    # Načtení všech lokací z databáze
    locations = Location.objects.all()
    # Předání dat do šablony
    return render(request, 'rezervace/location_list.html', {'locations': locations})

def location_detail(request, pk):
    # Načtení konkrétní lokace podle primárního klíče (pk)
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.location = location  # Spojení recenze s aktuální lokací
            review.save()
            return redirect('location_detail', pk=location.pk)
    else:
        form = ReviewForm()
    return render(request, 'rezervace/location_detail.html', {'location': location, 'form': form})

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

def reservation_list(request):
    reservations = Reservation.objects.all()  # Načtení všech rezervací
    return render(request, 'rezervace/reservation_list.html', {'reservations': reservations})

def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'rezervace/tournament_list.html', {'tournaments': tournaments})

def tournament_detail(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.method == 'POST':
        form = TournamentRegistrationForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            if tournament.participants.count() < tournament.capacity:
                participant.tournament = tournament
                participant.save()
                return redirect('tournament_detail', pk=tournament.pk)
            else:
                return render(request, 'rezervace/tournament_detail.html', {
                    'tournament': tournament,
                    'form': form,
                    'error': 'The tournament is full.'
                })
    else:
        form = TournamentRegistrationForm()
    return render(request, 'rezervace/tournament_detail.html', {'tournament': tournament, 'form': form})

