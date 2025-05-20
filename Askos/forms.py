from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from Askos.models import Cliente

class CodiceFiscaleLoginForm(forms.Form):
    codice_fiscale = forms.CharField(label="Codice Fiscale")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        codice_fiscale = cleaned_data.get("codice_fiscale")
        password = cleaned_data.get("password")

        try:
            cliente = Cliente.objects.get(cod_fiscale=codice_fiscale)
            user = authenticate(username=cliente.user.username, password=password)
            if user is None:
                raise forms.ValidationError("Credenziali non valide.")
            self.user = user
        except Cliente.DoesNotExist:
            raise forms.ValidationError("Codice fiscale non trovato.")

        return cleaned_data

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from Askos.models import Staff

class StaffLoginForm(forms.Form):
    codice_fiscale = forms.CharField(label="Codice Fiscale")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        cod_fiscale = cleaned_data.get("codice_fiscale")
        password = cleaned_data.get("password")

        try:
            # Recupera lo staff con quel codice fiscale
            staff = Staff.objects.get(cod_fiscale=cod_fiscale)
            # Recupera l'utente associato allo staff
            user = User.objects.get(email=staff.email)
            user_auth = authenticate(username=user.username, password=password)

            if user_auth is None:
                raise forms.ValidationError("Password non valida.")
            self.user = user_auth
        except (Staff.DoesNotExist, User.DoesNotExist):
            raise forms.ValidationError("Codice fiscale non trovato.")

        return cleaned_data


