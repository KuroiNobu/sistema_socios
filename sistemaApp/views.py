from functools import wraps

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from sistemaApp.models import Proveedores, Descuentos, Usuarios, Credenciales, Socios, Pagos, Cuotas, SolicitudIngreso
from sistemaApp.forms import (
    ProveedoresForm,
    DescuentosForm,
    UsuariosForm,
    CredencialesForm,
    SociosForm,
    PagosForm,
    CuotasForm,
    LoginForm,
    SocioPerfilForm,
    SolicitudIngresoForm,
)


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('auth_id'):
            messages.info(request, 'Inicia sesión para continuar.')
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('auth_id'):
            messages.info(request, 'Inicia sesión para continuar.')
            return redirect('login')
        if request.session.get('user_type') != 'admin':
            messages.warning(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('area_personal')
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
        'title': 'Solicitudes de ingreso',
        'description': 'Revisa las solicitudes para ser socio o proveedor.',
        'icon': 'fas fa-inbox',
        'primary_url': None,
        'primary_label': None,
        'secondary_url': 'solicitudes_ingreso',
        'secondary_label': 'Ver solicitudes',
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


SOCIO_ACTIONS = [
    {
        'title': 'Mi perfil',
        'description': 'Actualiza tus datos y mantente al día como socio.',
        'icon': 'fas fa-user-circle',
        'primary_url': 'perfil_socio',
        'primary_label': 'Editar perfil',
        'secondary_url': None,
        'secondary_label': None,
    },
    {
        'title': 'Mis pagos',
        'description': 'Consulta los pagos registrados a tu nombre.',
        'icon': 'fas fa-money-bill-wave',
        'primary_url': 'socio_pagos',
        'primary_label': 'Ver pagos',
        'secondary_url': None,
        'secondary_label': None,
    },
    {
        'title': 'Mis cuotas',
        'description': 'Revisa el estado de tus cuotas vigentes.',
        'icon': 'fas fa-calendar-check',
        'primary_url': 'socio_cuotas',
        'primary_label': 'Ver cuotas',
        'secondary_url': None,
        'secondary_label': None,
    },
    {
        'title': 'Mi credencial',
        'description': 'Visualiza tu credencial digital generada por administración.',
        'icon': 'fas fa-id-card',
        'primary_url': 'socio_credencial',
        'primary_label': 'Ver credencial',
        'secondary_url': None,
        'secondary_label': None,
    },
]


PROVEEDOR_ACTIONS = [
    {
        'title': 'Información de proveedor',
        'description': 'Contacta con administración para actualizar convenios o beneficios.',
        'icon': 'fas fa-store',
        'primary_url': None,
        'primary_label': None,
        'secondary_url': None,
        'secondary_label': None,
    },
]


# Create your views here.
def login_view(request):
    
    
    
    if request.session.get('auth_id'):
        if request.session.get('user_type') == 'admin':
            return redirect('panel')
        return redirect('area_personal')

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        usuario = Usuarios.objects.filter(email=email).first()
        if usuario:
            if usuario.passwd != password:
                messages.error(request, 'La contraseña ingresada no es correcta.')
            else:
                request.session.flush()
                request.session['auth_id'] = usuario.id_usuario
                request.session['auth_scope'] = 'usuario'
                request.session['user_name'] = usuario.nombre
                request.session['user_email'] = usuario.email
                request.session['user_type'] = 'admin'
                messages.success(request, f'Bienvenido {usuario.nombre}.')
                return redirect('panel')
        else:
            socio = Socios.objects.filter(email=email).first()
            if socio:
                if not socio.passwd or socio.passwd != password:
                    messages.error(request, 'La contraseña ingresada no es correcta.')
                else:
                    request.session.flush()
                    request.session['auth_id'] = socio.id_socio
                    request.session['auth_scope'] = 'socio'
                    request.session['socio_id'] = socio.id_socio
                    request.session['user_name'] = socio.nombre
                    request.session['user_email'] = socio.email
                    request.session['user_type'] = 'socio'
                    messages.success(request, f'Bienvenido {socio.nombre}.')
                    return redirect('area_personal')
            else:
                proveedor = Proveedores.objects.filter(email=email).first()
                if proveedor:
                    if not proveedor.passwd or proveedor.passwd != password:
                        messages.error(request, 'La contraseña ingresada no es correcta.')
                    else:
                        request.session.flush()
                        request.session['auth_id'] = proveedor.id_proveedor
                        request.session['auth_scope'] = 'proveedor'
                        request.session['proveedor_id'] = proveedor.id_proveedor
                        request.session['user_name'] = proveedor.nombre
                        request.session['user_email'] = proveedor.email
                        request.session['user_type'] = 'proveedor'
                        messages.success(request, f'Bienvenido {proveedor.nombre}.')
                        return redirect('area_personal')
                else:
                    messages.error(request, 'No encontramos una cuenta con el correo proporcionado.')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login')


@admin_required
def panel(request):
    context = {
        'acciones': ADMIN_ACTIONS,
        'titulo': 'Panel administrativo',
        'usuario': request.session.get('user_name', ''),
        'user_type': 'admin',
    }
    return render(request, 'panel.html', context)


@login_required
def area_personal(request):
    user_type = request.session.get('user_type', '')

    if user_type == 'admin':
        return redirect('panel')

    if user_type == 'socio':
        acciones = SOCIO_ACTIONS
    elif user_type == 'proveedor':
        acciones = PROVEEDOR_ACTIONS
    else:
        acciones = []

    context = {
        'acciones': acciones,
        'titulo': 'Mi área personal',
        'usuario': request.session.get('user_name', ''),
        'user_type': user_type,
    }
    return render(request, 'panel.html', context)


def obtener_socio_y_usuario(request):
    auth_scope = request.session.get('auth_scope')
    auth_id = request.session.get('auth_id')

    socio = None
    usuario = None

    if auth_scope == 'socio':
        socio = Socios.objects.filter(pk=auth_id).select_related('id_usuario').first()
        if socio:
            usuario = socio.id_usuario
    elif auth_scope == 'usuario':
        usuario = Usuarios.objects.filter(pk=auth_id).first()
        if usuario:
            socio = Socios.objects.filter(id_usuario=usuario).first()

    return socio, usuario


def inicio(request):
    form = SolicitudIngresoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '¡Gracias! Recibimos tu solicitud y nos pondremos en contacto pronto.')
            return redirect('inicio')
        else:
            messages.error(request, 'Revisa la información ingresada e inténtalo nuevamente.')

    context = {
        'form_solicitud': form,
    }
    return render(request, 'index.html', context)


@login_required
def perfil_socio(request):
    user_type = request.session.get('user_type')

    if user_type != 'socio':
        messages.info(request, 'Solo un administrador puede asignarte el rol de socio. Contacta a administración.')
        return redirect('area_personal')

    socio, usuario = obtener_socio_y_usuario(request)

    if not socio:
        messages.info(request, 'Aún no tienes un perfil de socio asignado. Contacta a administración.')
        return redirect('area_personal')

    form = SocioPerfilForm(request.POST or None, instance=socio)

    if request.method == 'POST' and form.is_valid():
        socio_actualizado = form.save(usuario)
        request.session['user_name'] = socio_actualizado.nombre
        request.session['user_email'] = socio_actualizado.email
        messages.success(request, 'Tu información de socio se guardó correctamente.')
        return redirect('area_personal')

    context = {
        'form': form,
        'titulo': 'Mi perfil de socio',
        'tiene_registro': socio is not None,
    }
    return render(request, 'perfil_socio.html', context)


@login_required
def socio_pagos(request):
    socio, _ = obtener_socio_y_usuario(request)

    if not socio:
        messages.info(request, 'Necesitas completar tu perfil de socio para ver tus pagos.')
        return redirect('perfil_socio')

    pagos = Pagos.objects.filter(socio=socio).order_by('-fecha_pago')
    context = {
        'titulo': 'Mis pagos',
        'socio': socio,
        'pagos': pagos,
    }
    return render(request, 'socios/pagos.html', context)


@login_required
def socio_cuotas(request):
    socio, _ = obtener_socio_y_usuario(request)

    if not socio:
        messages.info(request, 'Necesitas completar tu perfil de socio para ver tus cuotas.')
        return redirect('perfil_socio')

    cuotas = Cuotas.objects.filter(id_pago__socio=socio).select_related('id_pago').order_by('-fecha_vencimiento')
    context = {
        'titulo': 'Mis cuotas',
        'socio': socio,
        'cuotas': cuotas,
    }
    return render(request, 'socios/cuotas.html', context)


@login_required
def socio_credencial(request):
    socio, _ = obtener_socio_y_usuario(request)

    if not socio:
        messages.info(request, 'Necesitas completar tu perfil de socio para acceder a tu credencial.')
        return redirect('perfil_socio')

    credencial = Credenciales.objects.filter(id_socio=socio).first()
    qr_img = None
    payload_json = None

    if credencial:
        payload = {
            "type": "credentials",
            "id": credencial.pk,
            "user": socio.nombre,
            "note": getattr(credencial, "codigo_qr", ""),
        }
        payload_json = json.dumps(payload, ensure_ascii=False)

        qr = qrcode.QRCode(box_size=8, border=3)
        qr.add_data(payload_json)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        qr_img = f"data:image/png;base64,{b64}"

    context = {
        'titulo': 'Mi credencial',
        'socio': socio,
        'credencial': credencial,
        'qr_img': qr_img,
        'payload_json': payload_json,
    }
    return render(request, 'socios/credencial.html', context)

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
    usuarios = Usuarios.objects.all().order_by('id_usuario')
    data =  {
        'titulo': 'Lista de Usuarios',
        'usuarios': usuarios,
    }
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
def solicitudes_ingreso(request):
    filtro_tipo = request.GET.get('tipo', '').strip()
    solicitudes = SolicitudIngreso.objects.all()

    if filtro_tipo in dict(SolicitudIngreso.TIPO_CHOICES):
        solicitudes = solicitudes.filter(tipo=filtro_tipo)

    solicitudes = solicitudes.order_by('-fecha_solicitud')

    context = {
        'titulo': 'Solicitudes de ingreso',
        'solicitudes': solicitudes,
        'filtro_tipo': filtro_tipo,
        'tipos': SolicitudIngreso.TIPO_CHOICES,
    }
    return render(request, 'sistemas/solicitudes.html', context)


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