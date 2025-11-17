import base64
from datetime import date, datetime
import io
import json
from decimal import Decimal
from functools import wraps

import qrcode
import xlwt
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

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
    FiltroSociosForm,
    FiltroProveedoresForm,
)

EXPORT_DATE_FORMAT = '%d/%m/%Y'


def _format_cell(value):
    if value is None:
        return ''
    if isinstance(value, (datetime, date)):
        return value.strftime(EXPORT_DATE_FORMAT)
    if isinstance(value, Decimal):
        return float(value)
    return value


def _build_excel_response(filename, headers, rows):
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('Datos')

    header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_colour gray25;')
    normal_style = xlwt.easyxf('align: horiz left;')

    for col_index, header in enumerate(headers):
        sheet.write(0, col_index, header, header_style)
        sheet.col(col_index).width = 4000

    for row_index, row in enumerate(rows, start=1):
        for col_index, cell in enumerate(row):
            sheet.write(row_index, col_index, _format_cell(cell), normal_style)

    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)

    response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def _build_pdf_response(filename, title, headers, rows):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()

    elements = [Paragraph(title, styles['Heading2']), Spacer(1, 12)]

    table_data = [headers] + [[str(_format_cell(cell)) for cell in row] for row in rows]
    table = Table(table_data, hAlign='LEFT', repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#cccccc')),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def _filtrar_socios_queryset(request):
    form = FiltroSociosForm(request.GET or None)
    socios_qs = Socios.objects.all().order_by('nombre')

    if form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        if nombre:
            socios_qs = socios_qs.filter(
                Q(nombre__icontains=nombre) | Q(apellido__icontains=nombre)
            )

        email = form.cleaned_data.get('email')
        if email:
            socios_qs = socios_qs.filter(email__icontains=email)

        telefono = form.cleaned_data.get('telefono')
        if telefono:
            socios_qs = socios_qs.filter(telefono__icontains=telefono)

        inicio = form.cleaned_data.get('fecha_inicio')
        if inicio:
            socios_qs = socios_qs.filter(fecha_registro__gte=inicio)

        fin = form.cleaned_data.get('fecha_fin')
        if fin:
            socios_qs = socios_qs.filter(fecha_registro__lte=fin)

    return socios_qs, form


def inicio(request):
    form = SolicitudIngresoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu solicitud fue enviada. Te contactaremos pronto.')
            return redirect('inicio')
        messages.error(request, 'Revisa la información ingresada e inténtalo nuevamente.')

    context = {
        'form_solicitud': form,
    }
    return render(request, 'index.html', context)


def solicitud_ingreso_publico(request):
    form = SolicitudIngresoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu solicitud fue enviada. Te contactaremos pronto.')
            return redirect('solicitud_ingreso')
        messages.error(request, 'Revisa la información ingresada e inténtalo nuevamente.')

    context = {
        'form_solicitud': form,
    }
    return render(request, 'solicitud.html', context)


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
        'title': 'Mis descuentos',
        'description': 'Consulta y gestiona los descuentos que ofreces a la comunidad.',
        'icon': 'fas fa-gift',
        'primary_url': 'proveedor_descuentos',
        'primary_label': 'Ver descuentos',
        'secondary_url': None,
        'secondary_label': None,
    },
    {
        'title': 'Pagos registrados',
        'description': 'Revisa el historial de pagos realizados por los socios.',
        'icon': 'fas fa-money-check-alt',
        'primary_url': 'proveedor_pagos',
        'primary_label': 'Ver pagos',
        'secondary_url': None,
        'secondary_label': None,
    },
    {
        'title': 'Cuotas programadas',
        'description': 'Monitorea el estado de las cuotas asociadas a los socios.',
        'icon': 'fas fa-calendar-alt',
        'primary_url': 'proveedor_cuotas',
        'primary_label': 'Ver cuotas',
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


def obtener_proveedor(request):
    if request.session.get('auth_scope') != 'proveedor':
        return None
    auth_id = request.session.get('auth_id')
    if not auth_id:
        return None

    return Proveedores.objects.filter(id_proveedor=auth_id).first()


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
    user_type = request.session.get('user_type')

    if user_type != 'socio':
        messages.info(request, 'Esta sección es exclusiva para socios registrados.')
        return redirect('area_personal')

    socio, _ = obtener_socio_y_usuario(request)
    if not socio:
        messages.info(request, 'Aún no tienes un perfil de socio asignado. Contacta a administración.')
        return redirect('area_personal')

    pagos = Pagos.objects.filter(socio=socio).order_by('-fecha_pago')
    context = {
        'titulo': 'Mis pagos',
        'socio': socio,
        'pagos': pagos,
    }
    return render(request, 'socios/pagos.html', context)


@login_required
def socio_cuotas(request):
    user_type = request.session.get('user_type')

    if user_type != 'socio':
        messages.info(request, 'Esta sección es exclusiva para socios registrados.')
        return redirect('area_personal')

    socio, _ = obtener_socio_y_usuario(request)
    if not socio:
        messages.info(request, 'Aún no tienes un perfil de socio asignado. Contacta a administración.')
        return redirect('area_personal')

    cuotas = (
        Cuotas.objects
        .filter(id_pago__socio=socio)
        .select_related('id_pago')
        .order_by('-fecha_vencimiento')
    )

    context = {
        'titulo': 'Mis cuotas',
        'socio': socio,
        'cuotas': cuotas,
    }
    return render(request, 'socios/cuotas.html', context)


@login_required
def exportar_mis_pagos_excel(request):
    if request.session.get('user_type') != 'socio':
        messages.info(request, 'Esta sección es exclusiva para socios registrados.')
        return redirect('area_personal')

    socio, _ = obtener_socio_y_usuario(request)
    if not socio:
        messages.info(request, 'Aún no tienes un perfil de socio asignado. Contacta a administración.')
        return redirect('area_personal')

    pagos = Pagos.objects.filter(socio=socio).order_by('-fecha_pago')
    headers = ['ID', 'Monto', 'Fecha de pago']
    rows = [[p.id_pago, p.monto, p.fecha_pago] for p in pagos]
    return _build_excel_response('mis_pagos.xls', headers, rows)


@login_required
def exportar_mis_pagos_pdf(request):
    if request.session.get('user_type') != 'socio':
        messages.info(request, 'Esta sección es exclusiva para socios registrados.')
        return redirect('area_personal')

    socio, _ = obtener_socio_y_usuario(request)
    if not socio:
        messages.info(request, 'Aún no tienes un perfil de socio asignado. Contacta a administración.')
        return redirect('area_personal')

    pagos = Pagos.objects.filter(socio=socio).order_by('-fecha_pago')
    headers = ['ID', 'Monto', 'Fecha de pago']
    rows = [[p.id_pago, p.monto, p.fecha_pago] for p in pagos]
    return _build_pdf_response('mis_pagos.pdf', 'Mis pagos', headers, rows)


@login_required
def exportar_mis_cuotas_excel(request):
    if request.session.get('user_type') != 'socio':
        messages.info(request, 'Esta sección es exclusiva para socios registrados.')
        return redirect('area_personal')

    socio, _ = obtener_socio_y_usuario(request)
    if not socio:
        messages.info(request, 'Aún no tienes un perfil de socio asignado. Contacta a administración.')
        return redirect('area_personal')

    cuotas = (
        Cuotas.objects
        .filter(id_pago__socio=socio)
        .select_related('id_pago')
        .order_by('-fecha_vencimiento')
    )
    headers = ['ID', 'Monto', 'Fecha de vencimiento', 'Estado']
    rows = [
        [c.id_cuota, c.monto, c.fecha_vencimiento, 'Pagada' if c.pagado else 'Pendiente']
        for c in cuotas
    ]
    return _build_excel_response('mis_cuotas.xls', headers, rows)


@login_required
def exportar_mis_cuotas_pdf(request):
    if request.session.get('user_type') != 'socio':
        messages.info(request, 'Esta sección es exclusiva para socios registrados.')
        return redirect('area_personal')

    socio, _ = obtener_socio_y_usuario(request)
    if not socio:
        messages.info(request, 'Aún no tienes un perfil de socio asignado. Contacta a administración.')
        return redirect('area_personal')

    cuotas = (
        Cuotas.objects
        .filter(id_pago__socio=socio)
        .select_related('id_pago')
        .order_by('-fecha_vencimiento')
    )
    headers = ['ID', 'Monto', 'Fecha de vencimiento', 'Estado']
    rows = [
        [c.id_cuota, c.monto, c.fecha_vencimiento, 'Pagada' if c.pagado else 'Pendiente']
        for c in cuotas
    ]
    return _build_pdf_response('mis_cuotas.pdf', 'Mis cuotas', headers, rows)

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


@login_required
def proveedor_descuentos(request):
    if request.session.get('user_type') != 'proveedor':
        messages.info(request, 'Esta sección es exclusiva para proveedores registrados.')
        return redirect('area_personal')

    proveedor = obtener_proveedor(request)
    if not proveedor:
        messages.info(request, 'No encontramos tu información de proveedor. Contacta a administración.')
        return redirect('area_personal')

    descuentos = Descuentos.objects.filter(proveedor=proveedor).select_related('proveedor').order_by('-id_descuento')
    context = {
        'titulo': 'Mis descuentos',
        'proveedor': proveedor,
        'descuentos': descuentos,
    }
    return render(request, 'proveedores/descuentos.html', context)


@login_required
def proveedor_pagos(request):
    if request.session.get('user_type') != 'proveedor':
        messages.info(request, 'Esta sección es exclusiva para proveedores registrados.')
        return redirect('area_personal')

    proveedor = obtener_proveedor(request)
    if not proveedor:
        messages.info(request, 'No encontramos tu información de proveedor. Contacta a administración.')
        return redirect('area_personal')

    pagos = Pagos.objects.select_related('socio').order_by('-fecha_pago')
    context = {
        'titulo': 'Pagos registrados',
        'proveedor': proveedor,
        'pagos': pagos,
    }
    return render(request, 'proveedores/pagos.html', context)


@login_required
def proveedor_cuotas(request):
    if request.session.get('user_type') != 'proveedor':
        messages.info(request, 'Esta sección es exclusiva para proveedores registrados.')
        return redirect('area_personal')

    proveedor = obtener_proveedor(request)
    if not proveedor:
        messages.info(request, 'No encontramos tu información de proveedor. Contacta a administración.')
        return redirect('area_personal')

    cuotas = Cuotas.objects.select_related('id_pago__socio').order_by('-fecha_vencimiento')
    context = {
        'titulo': 'Cuotas programadas',
        'proveedor': proveedor,
        'cuotas': cuotas,
    }
    return render(request, 'proveedores/cuotas.html', context)

@admin_required
def proveedores(request):
    form = FiltroProveedoresForm(request.GET or None)
    proveedores = Proveedores.objects.all().order_by('nombre')

    if form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        if nombre:
            proveedores = proveedores.filter(
                Q(nombre__icontains=nombre) | Q(apellido__icontains=nombre)
            )

        email = form.cleaned_data.get('email')
        if email:
            proveedores = proveedores.filter(email__icontains=email)

        tipo = form.cleaned_data.get('tipo_descuento')
        if tipo:
            proveedores = proveedores.filter(tipo_descuento__icontains=tipo)

    data = {
        'titulo': 'Lista de Proveedores',
        'proveedores': proveedores,
        'filtro_form': form,
    }
    return render(request, 'sistemas/proveedores.html', data)


@admin_required
def exportar_proveedores_excel(request):
    proveedores_qs = Proveedores.objects.all().order_by('nombre')
    headers = ['ID', 'Nombre completo', 'Email', 'Tipo de descuento', 'Fecha de descuento']
    rows = [
        [
            prov.id_proveedor,
            f"{prov.nombre} {prov.apellido or ''}".strip(),
            prov.email or '',
            prov.tipo_descuento or '',
            prov.fecha_descuento,
        ]
        for prov in proveedores_qs
    ]
    return _build_excel_response('proveedores.xls', headers, rows)


@admin_required
def exportar_proveedores_pdf(request):
    proveedores_qs = Proveedores.objects.all().order_by('nombre')
    headers = ['ID', 'Nombre completo', 'Email', 'Tipo de descuento', 'Fecha de descuento']
    rows = [
        [
            prov.id_proveedor,
            f"{prov.nombre} {prov.apellido or ''}".strip(),
            prov.email or '',
            prov.tipo_descuento or '',
            prov.fecha_descuento,
        ]
        for prov in proveedores_qs
    ]
    return _build_pdf_response('proveedores.pdf', 'Lista de Proveedores', headers, rows)


@admin_required
def crearProveedores(request):
    form = ProveedoresForm()
    data = {
        'titulo': 'Crear Proveedor',
        'form': form,
        'ruta': '/sistemas/proveedores/',
    }
    if request.method == 'POST':
        form = ProveedoresForm(request.POST, request.FILES)
        if form.is_valid():
            admin_id = request.session.get('auth_id')
            admin_user = Usuarios.objects.filter(pk=admin_id, tipo='admin').first()
            if not admin_user:
                messages.error(request, 'No se pudo identificar al administrador que crea el proveedor.')
                data['form'] = form
            else:
                FileSystemStorage(location='media/proveedores/')
                proveedor = form.save(commit=False)
                proveedor.id_usuario = admin_user
                proveedor.save()
                messages.success(request, 'Proveedor creado con éxito.')
                return redirect('proveedores')
        else:
            data['form'] = form
    return render(request, 'sistemas/createF.html', data)

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
    descuentos = Descuentos.objects.select_related('proveedor').all().order_by('-id_descuento')
    data = {
        'titulo': 'Lista de Descuentos',
        'descuentos': descuentos,
    }
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
    data = {
        'titulo': 'Lista de Usuarios',
        'usuarios': usuarios,
    }
    return render(request, 'sistemas/usuarios.html', data)


@admin_required
def exportar_usuarios_excel(request):
    usuarios_qs = Usuarios.objects.all().order_by('id_usuario')
    headers = ['ID', 'RUN', 'Nombre', 'Email']
    rows = [[u.id_usuario, u.run, u.nombre, u.email] for u in usuarios_qs]
    return _build_excel_response('usuarios.xls', headers, rows)


@admin_required
def exportar_usuarios_pdf(request):
    usuarios_qs = Usuarios.objects.all().order_by('id_usuario')
    headers = ['ID', 'RUN', 'Nombre', 'Email']
    rows = [[u.id_usuario, u.run, u.nombre, u.email] for u in usuarios_qs]
    return _build_pdf_response('usuarios.pdf', 'Lista de Usuarios', headers, rows)

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
    socios_qs, form = _filtrar_socios_queryset(request)

    data = {
        'titulo': 'Lista de Socios',
        'socios': socios_qs,
        'filtro_form': form,
    }
    return render(request, 'sistemas/socios.html', data)


@admin_required
def exportar_socios_excel(request):
    socios_qs, _ = _filtrar_socios_queryset(request)
    headers = ['ID', 'Nombre completo', 'Email', 'Teléfono', 'Fecha de registro']
    rows = [
        [
            socio.id_socio,
            f"{socio.nombre} {socio.apellido or ''}".strip(),
            socio.email,
            socio.telefono or '',
            socio.fecha_registro,
        ]
        for socio in socios_qs
    ]
    return _build_excel_response('socios.xls', headers, rows)


@admin_required
def exportar_socios_pdf(request):
    socios_qs, _ = _filtrar_socios_queryset(request)
    headers = ['ID', 'Nombre completo', 'Email', 'Teléfono', 'Fecha de registro']
    rows = [
        [
            socio.id_socio,
            f"{socio.nombre} {socio.apellido or ''}".strip(),
            socio.email,
            socio.telefono or '',
            socio.fecha_registro,
        ]
        for socio in socios_qs
    ]
    return _build_pdf_response('socios.pdf', 'Lista de Socios', headers, rows)

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
            admin_user = Usuarios.objects.filter(pk=request.session.get('auth_id')).first()
            if not admin_user:
                messages.error(request, 'No se pudo identificar al administrador que crea el socio.')
                data['form'] = form
            else:
                socio = form.save(commit=False)
                socio.id_usuario = admin_user
                socio.save()
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
    pagos = Pagos.objects.select_related('socio').all().order_by('-fecha_pago')
    data = {
        'titulo': 'Lista de Pagos',
        'pagos': pagos,
    }
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
    cuotas = Cuotas.objects.select_related('id_pago__socio').all().order_by('-fecha_vencimiento')
    data = {
        'titulo': 'Lista de Cuotas',
        'cuotas': cuotas,
    }
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



@admin_required
def credenciales(request):
    """
    Muestra la lista de Credenciales y genera (en memoria) un QR por cada registro.
    No utiliza POST para generar QR: cada usuario tiene su QR mostrado en la lista.
    """
    qs = Credenciales.objects.select_related('id_socio').all().order_by('-id_credencial')

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
        "cred_list": cred_list,
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