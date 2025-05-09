from django.contrib import admin
from .models import Location, Court

class CourtInline(admin.TabularInline):
    model = Court
    extra = 0
    readonly_fields = ('name', 'surface')  # Kurt se generuje automaticky, takže pole budou jen ke čtení

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'clay_courts', 'grass_courts', 'hard_courts')
    inlines = [CourtInline]