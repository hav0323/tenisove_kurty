from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('locations/', views.location_list, name='location_list'),
    path('locations/<int:pk>/', views.location_detail, name='location_detail'),
    path('reservations/new/', views.create_reservation, name='create_reservation'),
    path('reservations/', views.reservation_list, name='reservation_list'),  # Přidání cesty pro seznam rezervací
    path('ajax/load-courts/', views.ajax_load_courts, name='ajax_load_courts'),
    path('tournaments/', views.tournament_list, name='tournament_list'),
    path('tournaments/<int:pk>/', views.tournament_detail, name='tournament_detail'),
    path('reviews/', views.review_list, name='review_list'),  # URL pro seznam recenzí
    path('reviews/write/', views.write_review, name='write_review'),  # Without pre-selected location
    path('reviews/write/<int:location_id>/', views.write_review, name='write_review_with_location'),  # With pre-selected location
    path('tournaments/create/', views.create_tournament, name='create_tournament'),
    path('locations/create/', views.create_location, name='create_location'),
    path('reservations/select-location/', views.select_location, name='select_location'),
    path('reservations/new/<int:location_id>/', views.create_reservation, name='create_reservation'),
]