from django.urls import path

urlpatterns = [
    path('proveedores/', name='proveedores_list'),
    path('proveedores/<int:pk>/', name='proveedores_detail'),
]
