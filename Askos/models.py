from django.db import models

# ---------- LINGUA ----------
class Lingua(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

# ---------- GUIDA ----------
class Guida(models.Model):
    cod_fiscale = models.CharField(max_length=16, primary_key=True)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    eta = models.PositiveIntegerField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    lingue = models.ManyToManyField(Lingua, related_name='guide')  # N:M

    def __str__(self):
        return f"{self.nome} {self.cognome}"

# ---------- CLIENTE ----------
class Cliente(models.Model):
    cod_fiscale = models.CharField(max_length=16, primary_key=True)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    lingua_preferita = models.ForeignKey(Lingua, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nome} {self.cognome}"

# ---------- TOUR ----------
class Tour(models.Model):
    id_tour = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    data = models.DateField()
    durata = models.CharField(max_length=50)
    prezzo = models.DecimalField(max_digits=8, decimal_places=2)
    lingua = models.ForeignKey(Lingua, on_delete=models.SET_NULL, null=True)
    guida = models.ForeignKey(Guida, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nome} - {self.data}"

# ---------- PRENOTAZIONE ----------
class Prenotazione(models.Model):
    id_prenotazione = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    data_prenotazione = models.DateField(auto_now_add=True)
    num_partecipanti = models.PositiveIntegerField()

    def __str__(self):
        return f"Prenotazione #{self.id_prenotazione} - {self.cliente} → {self.tour}"
