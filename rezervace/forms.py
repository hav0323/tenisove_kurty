# filepath: /Users/jirihavlicek/school/4semestr/skj/Projekt/rezervacni_system/rezervace/forms.py
from django import forms
from .models import Reservation, Court, Location, Review, TournamentParticipant, Tournament
from django.forms.widgets import DateInput

from datetime import date, timedelta

class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=DateInput(attrs={'type': 'text', 'placeholder': 'DD.MM.YYYY'}),
        input_formats=['%d.%m.%Y'],  # Accepts dates in the format DD.MM.YYYY
        label="Date"
    )

    def __init__(self, *args, **kwargs):
        location_id = kwargs.pop('location_id', None)
        super().__init__(*args, **kwargs)
        if location_id:
            self.fields['court'].queryset = Court.objects.filter(location_id=location_id)

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

