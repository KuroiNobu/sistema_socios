from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from sistemaApp.models import Proveedores
from sistemaApp.forms import ProveedoresForm

# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def proveedores(request):
    proveedores = Proveedores.objects.all()
    data =  {'titulo': 'Lista de Proveedores', 'proveedores': proveedores}
    return render(request, 'sistema/proveedores.html', data)

def crearProveedores(request):
    form = ProveedoresForm()
    data = {
        'titulo':'Crear Proveedor',
        'form':form, 
        'ruta':'/producto/proveedores/'
    }
    if request.method == 'POST':
        form = ProveedoresForm(request.POST,request.FILES)
        if form.is_valid():
            FileSystemStorage(location='media/proveedores/')
            form.save()
            messages.success(request,'Proveedor creado con éxito.')
    return render(request,'producto/createF.html',data)

def editarProveedor(request,id):
    prov = Proveedores.objects.get(pk=id)
    form = ProveedoresForm(instance=prov)
    data = {
        'titulo':'Editar Proveedor',
        'form':form, 
        'ruta':'/producto/proveedores/'
    }
    if request.method == 'POST':
        form = ProveedoresForm(request.POST,request.FILES,instance=prov)
        if form.is_valid():
            form.save()
            messages.success(request,'Proveedor editado con éxito.')
    return render(request,'producto/createF.html',data)

def eliminarProveedor(request,id):
    prov = Proveedores.objects.get(pk=id)
    prov.delete()
    return redirect('/producto/proveedores')