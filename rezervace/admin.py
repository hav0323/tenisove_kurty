from django.contrib import admin
from .models import Location, Court, Tournament

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