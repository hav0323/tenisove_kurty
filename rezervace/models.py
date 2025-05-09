
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)  # Název střediska
    address = models.CharField(max_length=255)  # Adresa střediska
    city = models.CharField(max_length=100)  # Město
    clay_courts = models.PositiveIntegerField(default=0)  # Počet antukových kurtů
    grass_courts = models.PositiveIntegerField(default=0)  # Počet travnatých kurtů
    hard_courts = models.PositiveIntegerField(default=0)  # Počet kurtů s tvrdým povrchem

    def save(self, *args, **kwargs):
        # Zkontrolujeme, zda se jedná o nové středisko
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Pokud je nové, vytvoříme kurty
        if is_new:
            courts = []
            for i in range(self.clay_courts):
                courts.append(Court(location=self, name=f"Clay Court {i + 1}", surface="Clay"))
            for i in range(self.grass_courts):
                courts.append(Court(location=self, name=f"Grass Court {i + 1}", surface="Grass"))
            for i in range(self.hard_courts):
                courts.append(Court(location=self, name=f"Hard Court {i + 1}", surface="Hard"))
            Court.objects.bulk_create(courts)  # Vytvoříme všechny kurty najednou

    def __str__(self):
        return f"{self.name} ({self.city})"


class Court(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="courts")  # Propojení na středisko
    name = models.CharField(max_length=100)  # Např. "Clay Court 1"
    surface = models.CharField(max_length=50, choices=[  # Typ povrchu kurtu
        ('Clay', 'Clay'),
        ('Grass', 'Grass'),
        ('Hard', 'Hard')
    ])

    def __str__(self):
        return f"{self.name} - {self.location.name}"