from django.db import models
from django.contrib.auth.models import User

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
        return self.name 
    
class Reservation(models.Model):
    TIME_SLOTS = [
        ('14:00-15:00', '14:00-15:00'),
        ('15:00-16:00', '15:00-16:00'),
        ('16:00-17:00', '16:00-17:00'),
        ('17:00-18:00', '17:00-18:00'),
        ('18:00-19:00', '18:00-19:00'),
        ('19:00-20:00', '19:00-20:00'),
        ('20:00-21:00', '20:00-21:00'),
    ]

    location = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
        verbose_name="Location",
        null=True,  # Allow null values temporarily
        blank=True  # Allow blank values in forms
    )
    court = models.ForeignKey('Court', on_delete=models.CASCADE, related_name='reservations', verbose_name="Court")
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    date = models.DateField(verbose_name="Date")
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS, verbose_name="Time Slot")

    def __str__(self):
        return f"Reservation for {self.court.name} by {self.name} on {self.date} at {self.time_slot}"


class Review(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Location"
    )  # Propojení recenze na lokaci
    name = models.CharField(max_length=100, verbose_name="Name")  # Jméno autora recenze
    rating = models.PositiveIntegerField(
        verbose_name="Rating",
        choices=[(i, str(i)) for i in range(1, 6)]  # Hodnocení od 1 do 5
    )
    comment = models.TextField(verbose_name="Comment")  # Text recenze

    def __str__(self):
        return f"Review by {self.name} for {self.location.name} - {self.rating} stars"


class Tournament(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="tournaments",
        verbose_name="Location"
    )
    name = models.CharField(max_length=100, verbose_name="Tournament Name")
    date = models.DateField(verbose_name="Date")
    capacity = models.PositiveIntegerField(verbose_name="Capacity")

    def __str__(self):
        return self.name


class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="participants",
        verbose_name="Tournament"
    )
    name = models.CharField(max_length=100, verbose_name="Name")
    birth_date = models.DateField(verbose_name="Date of Birth")

    def __str__(self):
        return f"{self.name} ({self.birth_date}) in {self.tournament.name}"