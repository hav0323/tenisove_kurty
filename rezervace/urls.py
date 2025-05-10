from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('locations/', views.location_list, name='location_list'),
    path('locations/<int:pk>/', views.location_detail, name='location_detail'),
    path('reservations/new/', views.create_reservation, name='create_reservation'),
    path('ajax/load-courts/', views.ajax_load_courts, name='ajax_load_courts'),  # AJAX URL
]