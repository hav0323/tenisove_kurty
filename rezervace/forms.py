# filepath: /Users/jirihavlicek/school/4semestr/skj/Projekt/rezervacni_system/rezervace/forms.py
from django import forms
from .models import Reservation, Court, Location, Review, TournamentParticipant

from datetime import date, timedelta

class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamicky generujeme seznam kurtů podle zvolené lokace
        if 'location' in self.data:
            try:
                location_id = int(self.data.get('location'))
                self.fields['court'].queryset = Court.objects.filter(location_id=location_id)
            except (ValueError, TypeError):
                self.fields['court'].queryset = Court.objects.none()
        elif self.instance.pk:
            self.fields['court'].queryset = self.instance.location.courts.all()
        else:
            self.fields['court'].queryset = Court.objects.none()

        # Dynamicky generujeme seznam povolených dat (dnes + 7 dní)
        today = date.today()
        choices = [(today + timedelta(days=i), (today + timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(7)]
        self.fields['date'].widget = forms.Select(choices=choices)

    def clean(self):
        cleaned_data = super().clean()
        court = cleaned_data.get('court')
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')

        # Zkontrolujeme, zda již existuje rezervace pro daný kurt, datum a časový slot
        if Reservation.objects.filter(court=court, date=date, time_slot=time_slot).exists():
            self.add_error(
                None,  # Přidáme chybu na úroveň formuláře (ne konkrétní pole)
                f"The court '{court.name}' is already reserved on {date} during {time_slot}."
            )

        return cleaned_data

    class Meta:
        model = Reservation
        fields = ['location', 'court', 'date', 'time_slot', 'name', 'email']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']

class TournamentRegistrationForm(forms.ModelForm):
    class Meta:
        model = TournamentParticipant
        fields = ['name', 'birth_date']

