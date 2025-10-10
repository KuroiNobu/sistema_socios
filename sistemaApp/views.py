from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from sistemaApp.models import Proveedores, Descuentos, Usuarios, Credenciales, Socios, Pagos, Cuotas
from sistemaApp.forms import ProveedoresForm, DescuentosForm, UsuariosForm, CredencialesForm, SociosForm, PagosForm, CuotasForm


# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def proveedores(request):
    proveedores = Proveedores.objects.all()
    data =  {'titulo': 'Lista de Proveedores', 'proveedores': proveedores}
    return render(request, 'sistemas/proveedores.html', data)

def crearProveedores(request):
    form = ProveedoresForm()
    data = {
        'titulo':'Crear Proveedor',
        'form':form, 
        'ruta':'/sistemas/proveedores/'
    }
    if request.method == 'POST':
        form = ProveedoresForm(request.POST,request.FILES)
        if form.is_valid():
            FileSystemStorage(location='media/proveedores/')
            form.save()
            messages.success(request,'Proveedor creado con éxito.')
    return render(request,'sistemas/createF.html',data)

def editarProveedor(request,id):
    prov = Proveedores.objects.get(pk=id)
    form = ProveedoresForm(instance=prov)
    data = {
        'titulo':'Editar Proveedor',
        'form':form, 
        'ruta':'/sistemas/proveedores/'
    }
    if request.method == 'POST':
        form = ProveedoresForm(request.POST,request.FILES,instance=prov)
        if form.is_valid():
            form.save()
            messages.success(request,'Proveedor editado con éxito.')
    return render(request,'sistemas/createF.html',data)

def eliminarProveedor(request,id):
    prov = Proveedores.objects.get(pk=id)
    prov.delete()
    return redirect('/sistemas/proveedores')


def descuentos(request):
    descuentos = Descuentos.objects.all()
    data =  {'titulo': 'Lista de Descuentos', 'descuentos': descuentos}
    return render(request, 'sistemas/descuentos.html', data)

def crearDescuentos(request):
    form = DescuentosForm()
    data = {
        'titulo':'Crear Descuento',
        'form':form, 
        'ruta':'/sistemas/descuentos/'
    }
    if request.method == 'POST':
        form = DescuentosForm(request.POST,request.FILES)
        if form.is_valid():
            FileSystemStorage(location='media/descuentos/')
            form.save()
            messages.success(request,'Descuento creado con éxito.')
    return render(request,'sistemas/createF.html',data)

def editarDescuentos(request,id):
    desc = Descuentos.objects.get(pk=id)
    form = DescuentosForm(instance=desc)
    data = {
        'titulo':'Editar Descuentos',
        'form':form, 
        'ruta':'/sistemas/descuentos/'
    }
    if request.method == 'POST':
        form = DescuentosForm(request.POST,request.FILES,instance=desc)
        if form.is_valid():
            form.save()
            messages.success(request,'Descuento editado con éxito.')
    return render(request,'sistemas/createF.html',data)

def eliminarDescuentos(request,id):
    desc = Descuentos.objects.get(pk=id)
    desc.delete()
    return redirect('/sistemas/descuentos')


def usuarios(request):
    usuarios = Usuarios.objects.all()
    data =  {'titulo': 'Lista de Usuarios', 'usuarios': usuarios}
    return render(request, 'sistemas/usuarios.html', data)

def crearUsuarios(request):
    form = UsuariosForm()
    data = {
        'titulo':'Crear Usuario',
        'form':form, 
        'ruta':'/sistemas/usuarios/'
    }
    if request.method == 'POST':
        form = UsuariosForm(request.POST,request.FILES)
        if form.is_valid():
            FileSystemStorage(location='media/usuarios/')
            form.save()
            messages.success(request,'Usuario creado con éxito.')
    return render(request,'sistemas/createF.html',data)

def editarUsuarios(request,id):
    user = Usuarios.objects.get(pk=id)
    form = UsuariosForm(instance=user)
    data = {
        'titulo':'Editar Usuario',
        'form':form, 
        'ruta':'/sistemas/usuarios/'
    }
    if request.method == 'POST':
        form = UsuariosForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'Usuario editado con éxito.')
    return render(request,'sistemas/createF.html',data)

def eliminarUsuarios(request,id):
    user = Usuarios.objects.get(pk=id)
    user.delete()
    return redirect('/sistemas/usuarios')

def credenciales(request):
    credenciales = Credenciales.objects.all()
    data =  {'titulo': 'Lista de Credenciales', 'credenciales': credenciales}
    return render(request, 'sistemas/credenciales.html', data)

def crearCredenciales(request):
    form = CredencialesForm()
    data = {
        'titulo':'Crear Credencial',
        'form':form, 
        'ruta':'/sistemas/credenciales/'
    }
    if request.method == 'POST':
        form = CredencialesForm(request.POST,request.FILES)
        if form.is_valid():
            FileSystemStorage(location='media/credenciales/')
            form.save()
            messages.success(request,'Credencial creada con éxito.')
    return render(request,'sistemas/createF.html',data)

def editarCredenciales(request,id):
    cred = Credenciales.objects.get(pk=id)
    form = CredencialesForm(instance=cred)
    data = {
        'titulo':'Editar Credencial',
        'form':form, 
        'ruta':'/sistemas/credenciales/'
    }
    if request.method == 'POST':
        form = CredencialesForm(request.POST,request.FILES,instance=cred)
        if form.is_valid():
            form.save()
            messages.success(request,'Credencial editada con éxito.')
    return render(request,'sistemas/createF.html',data)

def eliminarCredenciales(request,id):
    cred = Credenciales.objects.get(pk=id)
    cred.delete()
    return redirect('/sistemas/credenciales')

def socios(request):
    socios = Socios.objects.all()
    data =  {'titulo': 'Lista de Socios', 'socios': socios}
    return render(request, 'sistemas/socios.html', data)

def crearSocios(request):
    form = SociosForm()
    data = {
        'titulo':'Crear Socio',
        'form':form, 
        'ruta':'/sistemas/socios/'
    }
    if request.method == 'POST':
        form = SociosForm(request.POST,request.FILES)
        if form.is_valid():
            FileSystemStorage(location='media/socios/')
            form.save()
            messages.success(request,'Socio creado con éxito.')
    return render(request,'sistemas/createF.html',data)

def editarSocios(request,id):
    socio = Socios.objects.get(pk=id)
    form = SociosForm(instance=socio)
    data = {
        'titulo':'Editar Socio',
        'form':form, 
        'ruta':'/sistemas/socios/'
    }
    if request.method == 'POST':
        form = SociosForm(request.POST,request.FILES,instance=socio)
        if form.is_valid():
            form.save()
            messages.success(request,'Socio editado con éxito.')
    return render(request,'sistemas/createF.html',data)

def eliminarSocios(request,id):
    socio = Socios.objects.get(pk=id)
    socio.delete()
    return redirect('/sistemas/socios')

def pagos(request):
    pagos = Pagos.objects.all()
    data =  {'titulo': 'Lista de Pagos', 'pagos': pagos}
    return render(request, 'sistemas/pagos.html', data)

def crearPagos(request):
    form = PagosForm()
    data = {
        'titulo':'Crear Pago',
        'form':form, 
        'ruta':'/sistemas/pagos/'
    }
    if request.method == 'POST':
        form = PagosForm(request.POST,request.FILES)
        if form.is_valid():
            FileSystemStorage(location='media/pagos/')
            form.save()
            messages.success(request,'Pago creado con éxito.')
    return render(request,'sistemas/createF.html',data)

def editarPagos(request,id):    
    pago = Pagos.objects.get(pk=id)
    form = PagosForm(instance=pago)
    data = {
        'titulo':'Editar Pago',
        'form':form, 
        'ruta':'/sistemas/pagos/'
    }
    if request.method == 'POST':
        form = PagosForm(request.POST,request.FILES,instance=pago)
        if form.is_valid():
            form.save()
            messages.success(request,'Pago editado con éxito.')
    return render(request,'sistemas/createF.html',data)

def eliminarPagos(request,id):
    pago = Pagos.objects.get(pk=id)
    pago.delete()
    return redirect('/sistemas/pagos')

def cuotas(request):
    cuotas = Cuotas.objects.all()
    data =  {'titulo': 'Lista de Cuotas', 'cuotas': cuotas}
    return render(request, 'sistemas/cuotas.html', data)

def crearCuotas(request):
    form = CuotasForm()
    data = {
        'titulo':'Crear Cuota',
        'form':form, 
        'ruta':'/sistemas/cuotas/'
    }
    if request.method == 'POST':
        form = CuotasForm(request.POST,request.FILES)
        if form.is_valid():
            FileSystemStorage(location='media/cuotas/')
            form.save()
            messages.success(request,'Cuota creada con éxito.')
    return render(request,'sistemas/createF.html',data)

def editarCuotas(request,id):
    cuota = Cuotas.objects.get(pk=id)
    form = CuotasForm(instance=cuota)
    data = {
        'titulo':'Editar Cuota',
        'form':form, 
        'ruta':'/sistemas/cuotas/'
    }
    if request.method == 'POST':
        form = CuotasForm(request.POST,request.FILES,instance=cuota)
        if form.is_valid():
            form.save()
            messages.success(request,'Cuota editada con éxito.')
    return render(request,'sistemas/createF.html',data)

def eliminarCuotas(request,id):
    cuota = Cuotas.objects.get(pk=id)
    cuota.delete()
    return redirect('/sistemas/cuotas')



import qrcode
import io
import base64
import json
from datetime import datetime



def credenciales(request):
    """
    Muestra la lista de Credenciales y genera (en memoria) un QR por cada registro.
    No utiliza POST para generar QR: cada usuario tiene su QR mostrado en la lista.
    """
    qs = Credenciales.objects.all()
    cred_list = []

    for c in qs:

        payload = {
            "type": "credentials",
            "id": c.pk,
            "user": getattr(c, "usuario", ""),
            "note": getattr(c, "descripcion", "")
        }
        payload_json = json.dumps(payload, ensure_ascii=False)

        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(payload_json)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        qr_img = f"data:image/png;base64,{b64}"

        cred_list.append({
            "obj": c,
            "qr_img": qr_img,
            "payload_json": payload_json
        })

    context = {
        "titulo": "Lista de Credenciales",
        "cred_list": cred_list
    }
    return render(request, "sistemas/credenciales.html", context)


def descuentos_qr(request):
    """
    Lista descuentos y genera (en memoria) un QR asociado a cada registro.
    También permite generar un QR ad-hoc vía POST con campos: code, percent, expires.
    """
    qs = Descuentos.objects.all()
    desc_list = []

    for d in qs:
        payload = {
            "type": "discount",
            "id": d.pk,
            "code": getattr(d, "codigo", ""),
            "percent": getattr(d, "porcentaje", ""),
            "expires": str(getattr(d, "vigencia", ""))  # ajustar según campo
        }
        payload_json = json.dumps(payload, ensure_ascii=False)

        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(payload_json)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        qr_img = f"data:image/png;base64,{b64}"

        desc_list.append({
            "obj": d,
            "qr_img": qr_img,
            "payload_json": payload_json
        })

    # soporte para generar QR ad-hoc desde formulario
    qr_img_custom = None
    payload_custom = None
    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        percent = request.POST.get("percent", "").strip()
        expires = request.POST.get("expires", "").strip()
        payload_custom = {
            "type": "discount",
            "code": code,
            "percent": percent,
            "expires": expires
        }
        payload_json = json.dumps(payload_custom, ensure_ascii=False)
        qr = qrcode.QRCode(box_size=8, border=4)
        qr.add_data(payload_json)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        qr_img_custom = f"data:image/png;base64,{b64}"

    context = {
        "titulo": "Descuentos - QR",
        "desc_list": desc_list,
        "qr_img_custom": qr_img_custom,
        "payload_custom": json.dumps(payload_custom, ensure_ascii=False) if payload_custom else None
    }
    return render(request, "sistemas/descuentos_qr.html", context)