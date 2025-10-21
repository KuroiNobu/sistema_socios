from functools import wraps

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from sistemaApp.models import Proveedores, Descuentos, Usuarios, Credenciales, Socios, Pagos, Cuotas
from sistemaApp.forms import (
    ProveedoresForm,
    DescuentosForm,
    UsuariosForm,
    CredencialesForm,
    SociosForm,
    PagosForm,
    CuotasForm,
    LoginForm,
    RegistroUsuarioForm,
    SocioPerfilForm,
)


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.info(request, 'Inicia sesión para continuar.')
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.info(request, 'Inicia sesión para continuar.')
            return redirect('login')
        if request.session.get('user_type') != Usuarios.ADMIN:
            messages.warning(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('panel')
        return view_func(request, *args, **kwargs)

    return wrapper


ADMIN_ACTIONS = [
    {
        'title': 'Usuarios',
        'description': 'Crea y administra los usuarios autorizados.',
        'icon': 'fas fa-user-shield',
        'primary_url': 'crearusuarios',
        'primary_label': 'Registrar usuario',
        'secondary_url': 'usuarios',
        'secondary_label': 'Ver usuarios',
    },
    {
        'title': 'Socios',
        'description': 'Gestiona la información de los socios registrados.',
        'icon': 'fas fa-users',
        'primary_url': 'crearsocios',
        'primary_label': 'Registrar socio',
        'secondary_url': 'socios',
        'secondary_label': 'Ver socios',
    },
    {
        'title': 'Proveedores',
        'description': 'Administra los datos y convenios de proveedores.',
        'icon': 'fas fa-store',
        'primary_url': 'crearproveedores',
        'primary_label': 'Registrar proveedor',
        'secondary_url': 'proveedores',
        'secondary_label': 'Ver proveedores',
    },
    {
        'title': 'Descuentos',
        'description': 'Mantén los descuentos disponibles para los socios.',
        'icon': 'fas fa-gift',
        'primary_url': 'creardescuentos',
        'primary_label': 'Registrar descuento',
        'secondary_url': 'descuentos',
        'secondary_label': 'Ver descuentos',
    },
    {
        'title': 'Pagos',
        'description': 'Registra y revisa los pagos recibidos.',
        'icon': 'fas fa-money-bill-wave',
        'primary_url': 'crearpagos',
        'primary_label': 'Registrar pago',
        'secondary_url': 'pagos',
        'secondary_label': 'Ver pagos',
    },
    {
        'title': 'Cuotas',
        'description': 'Controla las cuotas programadas y su estado.',
        'icon': 'fas fa-calendar-check',
        'primary_url': 'crearcuotas',
        'primary_label': 'Registrar cuota',
        'secondary_url': 'cuotas',
        'secondary_label': 'Ver cuotas',
    },
    {
        'title': 'Credenciales',
        'description': 'Genera credenciales con código QR para socios.',
        'icon': 'fas fa-id-card',
        'primary_url': 'crearcredenciales',
        'primary_label': 'Registrar credencial',
        'secondary_url': 'credenciales',
        'secondary_label': 'Ver credenciales',
    },
]


USER_ACTIONS = [
    {
        'title': 'Perfil de socio',
        'description': 'Completa o actualiza tus datos para convertirte en socio.',
        'icon': 'fas fa-id-badge',
        'primary_url': 'perfil_socio',
        'primary_label': 'Gestionar mi perfil',
        'secondary_url': None,
        'secondary_label': None,
    },
]


# Create your views here.
def login_view(request):
    if request.session.get('user_id'):
        return redirect('panel')

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        try:
            usuario = Usuarios.objects.get(email=email)
        except Usuarios.DoesNotExist:
            messages.error(request, 'No encontramos una cuenta con el correo proporcionado.')
        else:
            if usuario.passwd != password:
                messages.error(request, 'La contraseña ingresada no es correcta.')
            else:
                request.session.flush()
                request.session['user_id'] = usuario.id_usuario
                request.session['user_name'] = usuario.nombre
                request.session['user_email'] = usuario.email
                request.session['user_type'] = usuario.tipo_usuario
                messages.success(request, f'Bienvenido {usuario.nombre}.')
                return redirect('panel')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login')


def registro_view(request):
    if request.session.get('user_id'):
        return redirect('panel')

    form = RegistroUsuarioForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        request.session.flush()
        request.session['user_id'] = usuario.id_usuario
        request.session['user_name'] = usuario.nombre
        request.session['user_email'] = usuario.email
        request.session['user_type'] = usuario.tipo_usuario
        messages.success(request, 'Cuenta creada con éxito. ¡Bienvenido!')
        return redirect('panel')

    return render(request, 'registro.html', {'form': form})


@login_required
def panel(request):
    user_type = request.session.get('user_type', Usuarios.ADMIN)
    acciones = ADMIN_ACTIONS if user_type == Usuarios.ADMIN else USER_ACTIONS
    context = {
        'acciones': acciones,
        'titulo': 'Panel principal',
        'usuario': request.session.get('user_name', ''),
        'user_type': user_type,
    }
    return render(request, 'panel.html', context)


def inicio(request):
    return render(request, 'index.html')


@login_required
def perfil_socio(request):
    if request.session.get('user_type') != Usuarios.NORMAL:
        messages.info(request, 'Esta sección es solo para usuarios estándar.')
        return redirect('panel')

    usuario = Usuarios.objects.get(pk=request.session['user_id'])
    socio = Socios.objects.filter(id_usuario=usuario).first()
    form = SocioPerfilForm(request.POST or None, instance=socio)

    if request.method == 'POST' and form.is_valid():
        form.save(usuario)
        messages.success(request, 'Tu información de socio se guardó correctamente.')
        return redirect('panel')

    context = {
        'form': form,
        'titulo': 'Mi perfil de socio',
        'tiene_registro': socio is not None,
    }
    return render(request, 'perfil_socio.html', context)

@admin_required
def proveedores(request):
    proveedores = Proveedores.objects.all()
    data =  {'titulo': 'Lista de Proveedores', 'proveedores': proveedores}
    return render(request, 'sistemas/proveedores.html', data)

@admin_required
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

@admin_required
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

@admin_required
def eliminarProveedor(request,id):
    prov = Proveedores.objects.get(pk=id)
    prov.delete()
    return redirect('/sistemas/proveedores')


@admin_required
def descuentos(request):
    descuentos = Descuentos.objects.all()
    data =  {'titulo': 'Lista de Descuentos', 'descuentos': descuentos}
    return render(request, 'sistemas/descuentos.html', data)

@admin_required
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

@admin_required
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

@admin_required
def eliminarDescuentos(request,id):
    desc = Descuentos.objects.get(pk=id)
    desc.delete()
    return redirect('/sistemas/descuentos')


@admin_required
def usuarios(request):
    usuarios = Usuarios.objects.all()
    data =  {'titulo': 'Lista de Usuarios', 'usuarios': usuarios}
    return render(request, 'sistemas/usuarios.html', data)

@admin_required
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
            form.save()
            messages.success(request,'Usuario creado con éxito.')
            return redirect('usuarios')
        else:
            # Si hay errores, mantener los datos del formulario
            data['form'] = form
    return render(request,'sistemas/createF.html',data)

@admin_required
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

@admin_required
def eliminarUsuarios(request,id):
    user = Usuarios.objects.get(pk=id)
    user.delete()
    return redirect('/sistemas/usuarios')

@admin_required
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

@admin_required
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

@admin_required
def eliminarCredenciales(request,id):
    cred = Credenciales.objects.get(pk=id)
    cred.delete()
    return redirect('/sistemas/credenciales')

@admin_required
def socios(request):
    socios = Socios.objects.all()
    data =  {'titulo': 'Lista de Socios', 'socios': socios}
    return render(request, 'sistemas/socios.html', data)

@admin_required
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
            form.save()
            messages.success(request,'Socio creado con éxito.')
            return redirect('socios')
        else:
            # Si hay errores, mantener los datos del formulario
            data['form'] = form
    return render(request,'sistemas/createF.html',data)

@admin_required
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

@admin_required
def eliminarSocios(request,id):
    socio = Socios.objects.get(pk=id)
    socio.delete()
    return redirect('/sistemas/socios')

@admin_required
def pagos(request):
    pagos = Pagos.objects.all()
    data =  {'titulo': 'Lista de Pagos', 'pagos': pagos}
    return render(request, 'sistemas/pagos.html', data)

@admin_required
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
            return redirect('/sistemas/pagos')
    return render(request,'sistemas/createF.html',data)

@admin_required
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
            return redirect('/sistemas/pagos')
    return render(request,'sistemas/createF.html',data)

@admin_required
def eliminarPagos(request,id):
    pago = Pagos.objects.get(pk=id)
    pago.delete()
    return redirect('/sistemas/pagos')

@admin_required
def cuotas(request):
    cuotas = Cuotas.objects.all()
    data =  {'titulo': 'Lista de Cuotas', 'cuotas': cuotas}
    return render(request, 'sistemas/cuotas.html', data)

@admin_required
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
            return redirect('/sistemas/cuotas')
    return render(request,'sistemas/createF.html',data)

@admin_required
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
            return redirect('/sistemas/cuotas')
    return render(request,'sistemas/createF.html',data)

@admin_required
def eliminarCuotas(request,id):
    cuota = Cuotas.objects.get(pk=id)
    cuota.delete()
    return redirect('/sistemas/cuotas')



import qrcode
import io
import base64
import json
from datetime import datetime



@admin_required
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


@admin_required
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