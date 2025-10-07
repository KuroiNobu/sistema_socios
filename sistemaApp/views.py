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

def crearProveedores(request):
    if request.method == 'POST':
        form = ProveedoresForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('proveedores')
    else:
        form = ProveedoresForm()
    return render(request, 'sistema/crear_proveedor.html', {'form': form})