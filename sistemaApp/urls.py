from django.urls import path
from sistemaApp import views

urlpatterns = [
    # Rutas para la gestión de proveedores
    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores/exportar/excel/', views.exportar_proveedores_excel, name='exportar_proveedores_excel'),
    path('proveedores/exportar/pdf/', views.exportar_proveedores_pdf, name='exportar_proveedores_pdf'),
    path('cproveedores/', views.crearProveedores, name='crearproveedores'),
    path('editarproveedores/<int:id>/', views.editarProveedor, name='editarproveedores'),
    path('eliminarproveedores/<int:id>/', views.eliminarProveedor, name='eliminarproveedores'),
    # Rutas para la gestión de descuentos
    path('descuentos/', views.descuentos, name='descuentos'),
    path('cdescuentos/', views.crearDescuentos, name='creardescuentos'),
    path('editardescuentos/<int:id>/', views.editarDescuentos, name='editardescuentos'),
    path('eliminardescuentos/<int:id>/', views.eliminarDescuentos, name='eliminardescuentos'),
    # Rutas para la gestión de usuarios
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/exportar/excel/', views.exportar_usuarios_excel, name='exportar_usuarios_excel'),
    path('usuarios/exportar/pdf/', views.exportar_usuarios_pdf, name='exportar_usuarios_pdf'),
    path('cusuarios/', views.crearUsuarios, name='crearusuarios'),
    path('editarusuarios/<int:id>/', views.editarUsuarios, name='editarusuarios'),
    path('eliminarusuarios/<int:id>/', views.eliminarUsuarios, name='eliminarusuarios'),
    path('solicitudes/', views.solicitudes_ingreso, name='solicitudes_ingreso'),
    # Rutas para la gestión de credenciales
    path('credenciales/', views.credenciales, name='credenciales'),
    path('ccredenciales/', views.crearCredenciales, name='crearcredenciales'),
    path('editarcredenciales/<int:id>/', views.editarCredenciales, name='editarcredenciales'),
    path('eliminarcredenciales/<int:id>/', views.eliminarCredenciales, name='eliminarcredenciales'),
    # Rutas para la gestión de socios
    path('socios/', views.socios, name='socios'),
    path('socios/exportar/excel/', views.exportar_socios_excel, name='exportar_socios_excel'),
    path('socios/exportar/pdf/', views.exportar_socios_pdf, name='exportar_socios_pdf'),
    path('csocios/', views.crearSocios, name='crearsocios'),
    path('editarsocios/<int:id>/', views.editarSocios, name='editarsocios'),
    path('eliminarsocios/<int:id>/', views.eliminarSocios, name='eliminarsocios'),
    # Rutas para la gestión de pagos
    path('pagos/', views.pagos, name='pagos'),
    path('cpagos/', views.crearPagos, name='crearpagos'),
    path('editarpagos/<int:id>/', views.editarPagos, name='editarpagos'),
    path('eliminarpagos/<int:id>/', views.eliminarPagos, name='eliminarpagos'),
    # Rutas para la gestión de cuotas
    path('cuotas/', views.cuotas, name='cuotas'),
    path('ccuotas/', views.crearCuotas, name='crearcuotas'),
    path('editarcuotas/<int:id>/', views.editarCuotas, name='editarcuotas'),
    path('eliminarcuotas/<int:id>/', views.eliminarCuotas, name='eliminarcuotas'),
]
