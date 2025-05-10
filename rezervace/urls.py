from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('locations/', views.location_list, name='location_list'),
    path('reservations/new/', views.create_reservation, name='create_reservation'),

]