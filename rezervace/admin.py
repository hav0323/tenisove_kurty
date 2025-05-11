from django.contrib import admin
from .models import Location, Court, Tournament, Reservation, Review, TournamentParticipant

class CourtInline(admin.TabularInline):
    model = Court
    extra = 0
    readonly_fields = ('name', 'surface')  # Kurt se generuje automaticky, takže pole budou jen ke čtení

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'clay_courts', 'grass_courts', 'hard_courts')
    inlines = [CourtInline]

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'date', 'capacity')
    list_filter = ('location', 'date')
    search_fields = ('name',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'court', 'date', 'time_slot')
    list_filter = ('court', 'date', 'time_slot')
    search_fields = ('name', 'email')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating')
    list_filter = ('location', 'rating')
    search_fields = ('name', 'comment')

@admin.register(TournamentParticipant)
class TournamentParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'tournament', 'birth_date')
    list_filter = ('tournament',)
    search_fields = ('name',)