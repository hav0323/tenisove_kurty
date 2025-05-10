# filepath: /Users/jirihavlicek/school/4semestr/skj/Projekt/rezervacni_system/rezervace/forms.py
from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['court', 'date', 'time', 'duration']