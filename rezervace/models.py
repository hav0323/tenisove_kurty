from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    address = models.CharField(max_length=255, verbose_name="Address")
    city = models.CharField(max_length=100, verbose_name="City")
    clay_courts = models.IntegerField(default=0, verbose_name="Clay Courts")
    grass_courts = models.IntegerField(default=0, verbose_name="Grass Courts")
    hard_courts = models.IntegerField(default=0, verbose_name="Hard Courts")

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

    def average_review_score(self):
        # Calculate the average rating of all reviews for this location
        avg_score = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg_score, 1) if avg_score else None  # Return None if no reviews exist

    def __str__(self):
        return self.name


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
    )
    name = models.CharField(max_length=100, verbose_name="Name")
    rating = models.PositiveIntegerField(
        verbose_name="Rating",
        choices=[
            (1, '1 star'),
            (2, '2 stars'),
            (3, '3 stars'),
            (4, '4 stars'),
            (5, '5 stars')
        ]
    )
    comment = models.TextField(verbose_name="Comment")

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