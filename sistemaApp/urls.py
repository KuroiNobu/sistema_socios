from django.urls import path
from sistemaApp.views import proveedores, crearProveedores, editarProveedor, eliminarProveedor, descuentos, crearDescuentos, editarDescuentos, eliminarDescuentos, pagos, crearPagos, editarPagos, eliminarPagos
from sistemaApp.views import usuarios, crearUsuarios, editarUsuarios, eliminarUsuarios, solicitudes_ingreso, credenciales, crearCredenciales, editarCredenciales, eliminarCredenciales, socios, crearSocios, editarSocios, eliminarSocios, cuotas, crearCuotas, editarCuotas, eliminarCuotas

urlpatterns = [
    # Rutas para la gestión de proveedores
    path('proveedores/', proveedores, name='proveedores'),
    path('cproveedores/', crearProveedores, name='crearproveedores'),
    path('editarproveedores/<int:id>/', editarProveedor, name='editarproveedores'),
    path('eliminarproveedores/<int:id>/', eliminarProveedor, name='eliminarproveedores'),
    # Rutas para la gestión de descuentos
    path('descuentos/', descuentos, name='descuentos'),
    path('cdescuentos/', crearDescuentos, name='creardescuentos'),
    path('editardescuentos/<int:id>/', editarDescuentos, name='editardescuentos'),
    path('eliminardescuentos/<int:id>/', eliminarDescuentos, name='eliminardescuentos'),
    # Rutas para la gestión de usuarios
    path('usuarios/', usuarios, name='usuarios'),
    path('cusuarios/', crearUsuarios, name='crearusuarios'),
    path('editarusuarios/<int:id>/', editarUsuarios, name='editarusuarios'),
    path('eliminarusuarios/<int:id>/', eliminarUsuarios, name='eliminarusuarios'),
    path('solicitudes/', solicitudes_ingreso, name='solicitudes_ingreso'),
    # Rutas para la gestión de credenciales
    path('credenciales/', credenciales, name='credenciales'),
    path('ccredenciales/', crearCredenciales, name='crearcredenciales'),
    path('editarcredenciales/<int:id>/', editarCredenciales, name='editarcredenciales'),
    path('eliminarcredenciales/<int:id>/', eliminarCredenciales, name='eliminarcredenciales'),
    # Rutas para la gestión de socios
    path('socios/', socios, name='socios'),
    path('csocios/', crearSocios, name='crearsocios'),
    path('editarsocios/<int:id>/', editarSocios, name='editarsocios'),
    path('eliminarsocios/<int:id>/', eliminarSocios, name='eliminarsocios'),
    # Rutas para la gestión de pagos
    path('pagos/', pagos, name='pagos'),
    path('cpagos/', crearPagos, name='crearpagos'),
    path('editarpagos/<int:id>/', editarPagos, name='editarpagos'),
    path('eliminarpagos/<int:id>/', eliminarPagos, name='eliminarpagos'),
    # Rutas para la gestión de cuotas
    path('cuotas/', cuotas, name='cuotas'),
    path('ccuotas/', crearCuotas, name='crearcuotas'),
    path('editarcuotas/<int:id>/', editarCuotas, name='editarcuotas'),
    path('eliminarcuotas/<int:id>/', eliminarCuotas, name='eliminarcuotas'),
]
