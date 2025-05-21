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
        return redirect('tour_list')

    return render(request, 'registrazione.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CodiceFiscaleLoginForm

from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import CodiceFiscaleLoginForm

def login_codice_fiscale(request):
    if request.method == 'POST':
        form = CodiceFiscaleLoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('tour_list')  # 👈 CAMBIATO QUI
    else:
        form = CodiceFiscaleLoginForm()

    return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from .models import Staff

def registrazione_staff_view(request):
    if request.method == 'POST':
        cod_fiscale = request.POST.get('cod_fiscale')
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        ruolo = request.POST.get('ruolo')

        # controllo codice fiscale duplicato
        if Staff.objects.filter(cod_fiscale=cod_fiscale).exists():
            return render(request, 'registrazione_staff.html', {'errore': 'Codice fiscale già registrato.'})

        Staff.objects.create(
            cod_fiscale=cod_fiscale,
            nome=nome,
            cognome=cognome,
            telefono=telefono,
            email=email,
            ruolo=ruolo
        )
        return redirect('login_staff')  # dopo registrazione, vai al login staff

    return render(request, 'registrazione_staff.html')

from django.contrib.auth import authenticate, login
from .forms import StaffLoginForm

def login_staff_view(request):
    if request.method == 'POST':
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('dashboard_staff')  # o un’altra pagina riservata
    else:
        form = StaffLoginForm()
    return render(request, 'login_staff.html', {'form': form})

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


from django.shortcuts import render
from .models import Tour, Cliente

def tour_list_view(request):
    tours = Tour.objects.all()
    lingua_filtrata = False

    if request.GET.get('lingua') == 'mia' and request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(user=request.user)
            tours = tours.filter(lingua=cliente.lingua_preferita)
            lingua_filtrata = True
        except Cliente.DoesNotExist:
            pass

    return render(request, 'tour_list.html', {
        'tours': tours,
        'lingua_filtrata': lingua_filtrata,
    })


from django.contrib.auth.decorators import login_required
from .models import Prenotazione

@login_required
def miei_tour_view(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
        prenotazioni = Prenotazione.objects.filter(cliente=cliente).select_related('tour')
    except Cliente.DoesNotExist:
        prenotazioni = []

    return render(request, 'miei_tour.html', {'prenotazioni': prenotazioni})
