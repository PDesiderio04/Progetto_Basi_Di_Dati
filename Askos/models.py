
from django.db import models
from django.contrib.auth.models import User

class Lingua(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Staff(models.Model):
    RUOLI = [
        ('guida', 'Guida'),
        ('driver', 'Driver'),
    ]

    cod_fiscale = models.CharField(max_length=16, primary_key=True)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    ruolo = models.CharField(max_length=10, choices=RUOLI)
    lingue = models.ManyToManyField(Lingua, related_name='staff_members')

    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.ruolo})"

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cod_fiscale = models.CharField(max_length=16, unique=True)
    telefono = models.CharField(max_length=20)
    lingua_preferita = models.ForeignKey(Lingua, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Tour(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    durata = models.CharField(max_length=50)
    prezzo = models.DecimalField(max_digits=8, decimal_places=2)
    lingua = models.ForeignKey(Lingua, on_delete=models.SET_NULL, null=True, related_name='tour')

    guide = models.ManyToManyField(
        Staff,
        limit_choices_to={'ruolo': 'guida'},
        related_name='tour_guide',
        blank=True
    )
    driver = models.ManyToManyField(
        Staff,
        limit_choices_to={'ruolo': 'driver'},
        related_name='tour_driver',
        blank=True
    )

    def __str__(self):
        return f"{self.nome} - {self.data}"

class Prenotazione(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='prenotazioni')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='prenotazioni')
    data_prenotazione = models.DateField(auto_now_add=True)
    num_partecipanti = models.PositiveIntegerField()

    def __str__(self):
        return f"Prenotazione di {self.cliente} per {self.tour}"

class Recensione(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    voto = models.PositiveIntegerField()  # 1-5 stelle
    commento = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cliente', 'tour')  # ogni cliente può recensire un tour una sola volta

    def __str__(self):
        return f"Recensione di {self.cliente} su {self.tour} - voto: {self.voto}"
