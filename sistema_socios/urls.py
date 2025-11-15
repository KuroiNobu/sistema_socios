"""
URL configuration for sistema_socios project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from sistemaApp.views import (
    inicio,
    login_view,
    logout_view,
    panel,
    perfil_socio,
    area_personal,
    socio_pagos,
    socio_cuotas,
    socio_credencial,
    proveedor_descuentos,
    proveedor_pagos,
    proveedor_cuotas,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',inicio,name='inicio'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('perfil-socio/', perfil_socio, name='perfil_socio'),
    path('panel/', panel, name='panel'),
        path('area-personal/', area_personal, name='area_personal'),
    path('mis-pagos/', socio_pagos, name='socio_pagos'),
    path('mis-cuotas/', socio_cuotas, name='socio_cuotas'),
    path('mi-credencial/', socio_credencial, name='socio_credencial'),
    path('proveedor/descuentos/', proveedor_descuentos, name='proveedor_descuentos'),
    path('proveedor/pagos/', proveedor_pagos, name='proveedor_pagos'),
    path('proveedor/cuotas/', proveedor_cuotas, name='proveedor_cuotas'),
    path('sistemas/',include('sistemaApp.urls'))
] + static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)