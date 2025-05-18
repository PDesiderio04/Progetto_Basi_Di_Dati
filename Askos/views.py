from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def registrazione_view(request):
    return render(request, 'registrazione.html')
