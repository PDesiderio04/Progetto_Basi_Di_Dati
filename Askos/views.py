from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def registrazione_view(request):
    return render(request, 'registrazione.html')
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Cliente, Lingua
from django.contrib.auth import login
from django.db.models import Max

def registrazione_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        cod_fiscale = request.POST['cod_fiscale']
        telefono = request.POST['telefono']
        lingua_id = int(request.POST['lingua'])

        if password1 != password2:
            return render(request, 'registrazione.html', {'errore': 'Le password non coincidono.'})

        # Controlla se codice fiscale già registrato
        if Cliente.objects.filter(cod_fiscale=cod_fiscale).exists():
            return render(request, 'registrazione.html', {'errore': 'Codice fiscale già registrato.'})

        # Assegna user_id partendo da 2
        ultimo_user_id = User.objects.aggregate(max_id=Max('id'))['max_id'] or 1
        user = User(id=ultimo_user_id + 1, username=username, email=email)
        user.set_password(password1)
        user.save()

        lingua = Lingua.objects.get(id=lingua_id)

        cliente = Cliente.objects.create(
            user=user,
            cod_fiscale=cod_fiscale,
            telefono=telefono,
            lingua_preferita=lingua
        )

        login(request, user)
        return redirect('index')

    return render(request, 'registrazione.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CodiceFiscaleLoginForm

def login_codice_fiscale(request):
    if request.method == 'POST':
        form = CodiceFiscaleLoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('index')
    else:
        form = CodiceFiscaleLoginForm()

    return render(request, 'login.html', {'form': form})

