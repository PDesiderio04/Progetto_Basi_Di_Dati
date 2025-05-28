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



from django.contrib.auth import authenticate, login
from .forms import StaffLoginForm

def login_staff_view(request):
    if request.method == 'POST':
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('tour_assegnati')  # o un’altra pagina riservata
    else:
        form = StaffLoginForm()
    return render(request, 'login_staff.html', {'form': form})

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


from django.shortcuts import render
from .models import Tour, Cliente

from datetime import date

def tour_list_view(request):
    tours = Tour.objects.all()
    lingua_filtrata = False
    today = date.today()

    prenotati_ids = []
    if request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(user=request.user)
            tours = tours.exclude(prenotazioni__cliente=cliente)
            prenotati_ids = Prenotazione.objects.filter(cliente=cliente).values_list('tour_id', flat=True)
            if request.GET.get('lingua') == 'mia':
                tours = Tour.objects.filter(lingua=cliente.lingua_preferita)
                lingua_filtrata = True
        except Cliente.DoesNotExist:
            pass

    return render(request, 'tour_list.html', {
        'tours': tours,
        'lingua_filtrata': lingua_filtrata,
        'prenotati_ids': prenotati_ids,
        'today': today,
    })




from django.contrib.auth.decorators import login_required
from .models import Prenotazione

from django.utils import timezone

from django.utils import timezone
from .models import Prenotazione, Recensione, Cliente

from django.utils import timezone
from .models import Prenotazione, Cliente, Recensione

@login_required
def miei_tour_view(request):
    today = timezone.now().date()

    try:
        cliente = Cliente.objects.get(user=request.user)
        prenotazioni = Prenotazione.objects.filter(cliente=cliente).select_related('tour')
        tour_recensiti_ids = Recensione.objects.filter(cliente=cliente).values_list('tour_id', flat=True)
    except Cliente.DoesNotExist:
        prenotazioni = []
        tour_recensiti_ids = []

    return render(request, 'miei_tour.html', {
        'prenotazioni': prenotazioni,
        'today': today,
        'tour_recensiti_ids': tour_recensiti_ids,
    })



from django.views.decorators.http import require_POST
from .models import Prenotazione, Tour
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

@require_POST
@login_required
def prenota_tour(request, tour_id):
    try:
        cliente = Cliente.objects.get(user=request.user)
        tour = Tour.objects.get(id=tour_id)

        # Evita doppie prenotazioni
        if not Prenotazione.objects.filter(cliente=cliente, tour=tour).exists():
            Prenotazione.objects.create(
                cliente=cliente,
                tour=tour,
                data_prenotazione=now().date(),
                num_partecipanti=1  # puoi estendere con un input in futuro
            )
    except (Cliente.DoesNotExist, Tour.DoesNotExist):
        pass

    return redirect('tour_list')

from django.views.decorators.http import require_POST

@require_POST
@login_required
def annulla_prenotazione(request, prenotazione_id):
    try:
        cliente = Cliente.objects.get(user=request.user)
        prenotazione = Prenotazione.objects.get(id=prenotazione_id, cliente=cliente)
        prenotazione.delete()
    except (Cliente.DoesNotExist, Prenotazione.DoesNotExist):
        pass

    return redirect('miei_tour')

from django.contrib import messages

@require_POST
@login_required
def prenota_tour(request, tour_id):
    try:
        cliente = Cliente.objects.get(user=request.user)
        tour = Tour.objects.get(id=tour_id)

        if not Prenotazione.objects.filter(cliente=cliente, tour=tour).exists():
            Prenotazione.objects.create(
                cliente=cliente,
                tour=tour,
                data_prenotazione=now().date(),
                num_partecipanti=1
            )
            messages.success(request, f"Hai prenotato il tour: {tour.nome}")
    except (Cliente.DoesNotExist, Tour.DoesNotExist):
        messages.error(request, "Prenotazione fallita.")

    return redirect('tour_list')

@require_POST
@login_required
def annulla_prenotazione(request, prenotazione_id):
    try:
        cliente = Cliente.objects.get(user=request.user)
        prenotazione = Prenotazione.objects.get(id=prenotazione_id, cliente=cliente)
        tour_nome = prenotazione.tour.nome
        prenotazione.delete()
        messages.success(request, f"Hai annullato la prenotazione per: {tour_nome}")
    except (Cliente.DoesNotExist, Prenotazione.DoesNotExist):
        messages.error(request, "Errore durante l'annullamento.")

    return redirect('miei_tour')
from django.shortcuts import render, redirect
from .models import Staff, Lingua
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def registrazione_staff_view(request):
    if request.method == 'POST':
        cod_fiscale = request.POST.get('cod_fiscale')
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        password = request.POST.get('password')
        ruolo = request.POST.get('ruolo')
        lingue_ids = request.POST.getlist('lingue')  # 👈 prende tutte le lingue selezionate

        # verifica se già esiste staff con quel codice fiscale
        if Staff.objects.filter(cod_fiscale=cod_fiscale).exists():
            return render(request, 'registrazione_staff.html', {'errore': 'Codice fiscale già registrato.'})

        # salva il record staff
        staff = Staff.objects.create(
            cod_fiscale=cod_fiscale,
            nome=nome,
            cognome=cognome,
            telefono=telefono,
            email=email,
            ruolo=ruolo
        )

        # associa lingue
        staff.lingue.set(lingue_ids)

        # (Opzionale) crea anche un account User associato
        user = User.objects.create(
            username=cod_fiscale,
            email=email,
            password=make_password(password)  # 👈 crittografia della password
        )

        # redirect dopo registrazione
        return redirect('login_staff')

    return render(request, 'registrazione_staff.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Tour, Staff

from django.shortcuts import render
from .models import Staff
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Staff

@login_required
def tour_assegnati_view(request):
    staff = get_object_or_404(Staff, cod_fiscale=request.user.username)
    tours = staff.tour_assegnati.all().order_by('data')  # solo i suoi tour
    return render(request, 'tour_assegnati.html', {'tours': tours})


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.success(request, "Logout effettuato con successo.")
    return redirect('index')

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tour, Cliente, Prenotazione, Recensione
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Tour, Recensione, Cliente

from django.contrib.auth.decorators import login_required

@login_required
def lascia_recensione(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    cliente = get_object_or_404(Cliente, user=request.user)

    oggi = timezone.now().date()

    # ✅ BLOCCO: il tour non è ancora avvenuto
    if tour.data > oggi:
        messages.error(request, "Non puoi recensire un tour che non hai ancora svolto.")
        return redirect('miei_tour')

    # ✅ BLOCCO: già recensito
    if Recensione.objects.filter(cliente=cliente, tour=tour).exists():
        messages.warning(request, "Hai già recensito questo tour.")
        return redirect('miei_tour')

    if request.method == 'POST':
        voto = int(request.POST['voto'])
        commento = request.POST['commento']

        Recensione.objects.create(
            cliente=cliente,
            tour=tour,
            voto=voto,
            commento=commento
        )
        messages.success(request, "Recensione inviata con successo.")
        return redirect('miei_tour')

    return render(request, 'lascia_recensione.html', {'tour': tour})


from django.shortcuts import render
from .models import Recensione

def recensioni_view(request):
    recensioni = Recensione.objects.select_related('cliente', 'tour').order_by('-data')
    return render(request, 'recensioni_pubbliche.html', {'recensioni': recensioni})

