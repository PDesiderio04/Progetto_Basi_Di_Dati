"""
URL configuration for BasiDiDati project.

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
from Askos.views import index, registrazione_view
from Askos.views import login_codice_fiscale
from Askos.views import login_staff_view, registrazione_staff_view
from Askos.views import index  # o dalla tua app
from django.contrib import admin
from django.urls import path
from Askos.views import tour_list_view
from Askos.views import miei_tour_view
from Askos.views import prenota_tour
from Askos.views import annulla_prenotazione
from Askos.views import tour_assegnati_view
from Askos.views import logout_view



urlpatterns = [
    path('', index, name='index'),  # questa è la root del sito
    path('login/', login_codice_fiscale, name='login'),
    path('registrazione/', registrazione_view, name='registrazione'),
    path('login-staff/', login_staff_view, name='login_staff'),
    path('registrazione-staff/', registrazione_staff_view, name='registrazione_staff'),
    path('admin/', admin.site.urls),
    path('tours/', tour_list_view, name='tour_list'),
    path('i-miei-tour/', miei_tour_view, name='miei_tour'),
    path('prenota/<int:tour_id>/', prenota_tour, name='prenota_tour'),
path('annulla-prenotazione/<int:prenotazione_id>/', annulla_prenotazione, name='annulla_prenotazione'),

    path('logout/', logout_view, name='logout'),

    path('staff/tour-assegnati/', tour_assegnati_view, name='tour_assegnati'),

]







