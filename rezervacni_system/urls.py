"""
URL configuration for rezervacni_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from rezervace import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('locations/', include('rezervace.urls')), 
    path('api/locations/', views.api_location_list, name='api_location_list'),
    path('api/tournaments/', views.api_tournament_list, name='api_tournament_list'),
    path('api/reservations/', views.api_reservation_list, name='api_reservation_list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.homepage, name='home'),

         
]
