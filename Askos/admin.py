from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Cliente, Staff, Lingua, Tour, Prenotazione, Recensione

# 🔹 Cliente admin
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'cod_fiscale', 'telefono', 'lingua_preferita')
    search_fields = ('cod_fiscale', 'user__username', 'telefono')
    list_filter = ('lingua_preferita',)

# 🔹 Staff admin
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('cod_fiscale', 'nome', 'cognome', 'ruolo', 'email', 'telefono')
    search_fields = ('cod_fiscale', 'nome', 'cognome', 'email')
    list_filter = ('ruolo',)

# 🔹 Lingua admin
@admin.register(Lingua)
class LinguaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

# 🔹 Tour admin
from django.contrib import admin
from .models import Tour, Staff

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data', 'prezzo']
    filter_horizontal = ['guide', 'driver', 'staff_assegnato']


# 🔹 Prenotazione admin
@admin.register(Prenotazione)
class PrenotazioneAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tour', 'data_prenotazione', 'num_partecipanti')
    search_fields = ('cliente__cod_fiscale', 'tour__nome')
    list_filter = ('data_prenotazione',)

# 🔹 Recensione admin
@admin.register(Recensione)
class RecensioneAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tour', 'voto', 'data')
    search_fields = ('cliente__cod_fiscale', 'tour__nome')
    list_filter = ('voto',)
