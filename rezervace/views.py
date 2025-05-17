from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm, ReviewForm, TournamentRegistrationForm, CreateTournamentForm, CreateLocationForm, LocationFilterForm, SelectLocationForm
from .models import Location, Court, Reservation, Tournament, Review

# Create your views here

@login_required
def location_list(request):
    form = LocationFilterForm(request.GET)  # Zpracování GET požadavku
    locations = Location.objects.all()

    if form.is_valid():
        city = form.cleaned_data.get('city')
        if city:
            locations = locations.filter(city__icontains=city)  # Filtrování podle města

    return render(request, 'rezervace/location_list.html', {'locations': locations, 'form': form})

@login_required
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

@login_required
def create_reservation(request, location_id=None):
    if location_id is None:
        # Redirect to the Select Location page if location_id is missing
        return HttpResponseRedirect(reverse('select_location_reservation'))

    if request.method == 'POST':
        form = ReservationForm(request.POST, location_id=location_id)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.location_id = location_id
            reservation.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(location_id=location_id)
    return render(request, 'rezervace/reservation_form.html', {'form': form})

def homepage(request):
    return render(request, 'rezervace/homepage.html')

@login_required
def reservation_list(request):
    reservations = Reservation.objects.all()  # Načtení všech rezervací
    return render(request, 'rezervace/reservation_list.html', {'reservations': reservations})

@login_required
def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'rezervace/tournament_list.html', {'tournaments': tournaments})

@login_required
def tournament_detail(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)

    if request.method == 'POST':
        form = TournamentRegistrationForm(request.POST, tournament=tournament)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.tournament = tournament
            participant.save()
            return redirect('tournament_detail', pk=tournament.pk)
    else:
        form = TournamentRegistrationForm(tournament=tournament)

    return render(request, 'rezervace/tournament_detail.html', {
        'tournament': tournament,
        'form': form,
    })

def review_list(request):
    reviews = Review.objects.all()  # Načtení všech recenzí
    return render(request, 'rezervace/review_list.html', {'reviews': reviews})

def write_review(request, location_id=None):
    if location_id is None:
        # Redirect to the Select Location page if location_id is missing
        return redirect('select_location_review')

    location = get_object_or_404(Location, pk=location_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, location_provided=True)
        if form.is_valid():
            review = form.save(commit=False)
            review.location = location  # Explicitly set the location
            review.save()
            return redirect('review_list')  # Redirect to the review list after submission
    else:
        form = ReviewForm(location_provided=True)

    return render(request, 'rezervace/write_review.html', {'form': form, 'location': location})

def create_tournament(request):
    if request.method == 'POST':
        form = CreateTournamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tournament_list')  # Redirect to the tournament list after creation
    else:
        form = CreateTournamentForm()
    return render(request, 'rezervace/create_tournament.html', {'form': form})

def create_location(request):
    if request.method == 'POST':
        form = CreateLocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')  # Redirect to the location list after creation
    else:
        form = CreateLocationForm()
    return render(request, 'rezervace/create_location.html', {'form': form})

def select_location(request, next_view):
    if request.method == 'POST':
        form = SelectLocationForm(request.POST)
        if form.is_valid():
            location_id = form.cleaned_data['location'].id
            return redirect(next_view, location_id=location_id)  # Přesměrování na zadaný pohled
    else:
        form = SelectLocationForm()
    return render(request, 'rezervace/select_location.html', {'form': form})



def api_location_list(request):
    locations = Location.objects.all()
    data = serialize('json', locations)
    return JsonResponse(data, safe=False)
def api_tournament_list(request):
    tournaments = Tournament.objects.all()  # Načtení všech turnajů
    data = serialize('json', tournaments, fields=('name', 'location', 'date', 'capacity'))
    return JsonResponse(data, safe=False)  # Vrácení dat ve formátu JSON
def api_reservation_list(request):
    reservations = Reservation.objects.all()  # Načtení všech rezervací
    data = serialize('json', reservations, fields=('court', 'date', 'time_slot', 'name', 'email'))
    return JsonResponse(data, safe=False)  # Vrácení dat ve formátu JSON
