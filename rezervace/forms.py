# filepath: /Users/jirihavlicek/school/4semestr/skj/Projekt/rezervacni_system/rezervace/forms.py
from django import forms
from .models import Reservation, Court, Location
from datetime import date, timedelta

class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamicky generujeme seznam povolených dat (dnes + 7 dní)
        today = date.today()
        choices = [(today + timedelta(days=i), (today + timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(7)]
        self.fields['date'].widget = forms.Select(choices=choices)

        # Filtrování kurtů podle zvoleného střediska
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

    class Meta:
        model = Reservation
        fields = ['location', 'court', 'date', 'time_slot', 'name', 'email']