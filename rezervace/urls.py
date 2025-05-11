from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('locations/', views.location_list, name='location_list'),
    path('locations/<int:pk>/', views.location_detail, name='location_detail'),
    path('reservations/', views.reservation_list, name='reservation_list'),  # Přidání cesty pro seznam rezervací
    path('tournaments/', views.tournament_list, name='tournament_list'),
    path('tournaments/<int:pk>/', views.tournament_detail, name='tournament_detail'),
    path('reviews/', views.review_list, name='review_list'),  # URL pro seznam recenzí
    path('tournaments/create/', views.create_tournament, name='create_tournament'),
    path('locations/create/', views.create_location, name='create_location'),
    path('reservations/select-location/', views.select_location, {'next_view': 'create_reservation'}, name='select_location_reservation'),
    path('reservations/new/<int:location_id>/', views.create_reservation, name='create_reservation'),
    path('reviews/select-location/', views.select_location, {'next_view': 'write_review'}, name='select_location_review'),
    path('reviews/write/<int:location_id>/', views.write_review, name='write_review'),
    path('api/locations/', views.api_location_list, name='api_location_list'),
    path('api/tournaments/', views.api_tournament_list, name='api_tournament_list'),
    path('api/reservations/', views.api_reservation_list, name='api_reservation_list'),
]