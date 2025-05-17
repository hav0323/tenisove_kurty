# filepath: /Users/jirihavlicek/school/4semestr/skj/Projekt/rezervacni_system/rezervace/forms.py
from django import forms
from .models import Reservation, Court, Location, Review, TournamentParticipant, Tournament
from django.forms.widgets import DateInput
from datetime import date, timedelta

class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        location_id = kwargs.pop('location_id', None)
        super().__init__(*args, **kwargs)

        # Dynamically generate date choices for the next 7 days
        today = date.today()
        date_choices = [(today + timedelta(days=i), (today + timedelta(days=i)).strftime('%d.%m.%Y')) for i in range(7)]
        self.fields['date'].choices = date_choices

        # Filter courts by location if location_id is provided
        if location_id:
            self.fields['court'].queryset = Court.objects.filter(location_id=location_id)

    date = forms.ChoiceField(
        label="Date",
        widget=forms.Select(attrs={'class': 'form-select'})  # Use a dropdown (scroll bar)
    )

    def clean(self):
        cleaned_data = super().clean()
        court = cleaned_data.get('court')
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')

        # Check if a reservation already exists for the same court, date, and time slot
        if Reservation.objects.filter(court=court, date=date, time_slot=time_slot).exists():
            raise forms.ValidationError(
                f"A reservation already exists for {court.name} on {date} at {time_slot}."
            )

        return cleaned_data

    class Meta:
        model = Reservation
        fields = ['court', 'date', 'time_slot', 'name', 'email']

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        location_provided = kwargs.pop('location_provided', False)
        super().__init__(*args, **kwargs)
        if location_provided:
            self.fields.pop('location')  # Remove the location field if it's already provided

    class Meta:
        model = Review
        fields = ['location', 'name', 'rating', 'comment']

class TournamentRegistrationForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=DateInput(attrs={'type': 'text', 'placeholder': 'DD.MM.YYYY'}),
        input_formats=['%d.%m.%Y'],  # Accepts dates in the format DD.MM.YYYY
        label="Birth Date"
    )

    def __init__(self, *args, **kwargs):
        self.tournament = kwargs.pop('tournament', None)  # Pass the tournament instance
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        birth_date = cleaned_data.get('birth_date')

        # Check if the participant is already registered for the tournament
        if TournamentParticipant.objects.filter(
            tournament=self.tournament, name=name, birth_date=birth_date
        ).exists():
            raise forms.ValidationError(
                f"{name} is already registered for this tournament."
            )

        # Check if the tournament has reached its capacity
        if self.tournament.participants.count() >= self.tournament.capacity:
            raise forms.ValidationError(
                "The tournament is full. No more participants can register."
            )

        return cleaned_data

    class Meta:
        model = TournamentParticipant
        fields = ['name', 'birth_date']

class CreateTournamentForm(forms.ModelForm):
    date = forms.DateField(
        widget=DateInput(attrs={'type': 'text', 'placeholder': 'DD.MM.YYYY'}),
        input_formats=['%d.%m.%Y'],  # Accepts dates in the format DD.MM.YYYY
        label="Date:"
    )

    class Meta:
        model = Tournament
        fields = ['name', 'location', 'date', 'capacity']

    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get('location')
        date = cleaned_data.get('date')

        # Check if a tournament already exists at the same location and date
        if Tournament.objects.filter(location=location, date=date).exists():
            self.add_error(
                None,
                f"A tournament is already scheduled at {location.name} on {date}."
            )

        return cleaned_data

class CreateLocationForm(forms.ModelForm):
    clay_courts = forms.IntegerField(
        min_value=0,  # Minimum value is 0
        label="Number of Clay Courts",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    grass_courts = forms.IntegerField(
        min_value=0,  # Minimum value is 0
        label="Number of Grass Courts",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    hard_courts = forms.IntegerField(
        min_value=0,  # Minimum value is 0
        label="Number of Hard Courts",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Location
        fields = ['name', 'address', 'city', 'clay_courts', 'grass_courts', 'hard_courts']

class LocationFilterForm(forms.Form):
    city = forms.CharField(
        max_length=100,
        required=False,
        label="City",
        widget=forms.TextInput(attrs={'placeholder': 'Enter city name'})
    )

class SelectLocationForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        label="Select Location",
        empty_label="Choose a location"
    )

