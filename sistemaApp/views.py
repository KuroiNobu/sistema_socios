from django.shortcuts import render
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from sistemaApp.models import Proveedores

# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def proveedores(request):
    proveedores = Proveedores.objects.all()
    data =  {'titulo': 'Lista de Proveedores', 'proveedores': proveedores}
    return render(request, 'sistema/proveedores.html', data)