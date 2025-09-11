from django.db import models

# Create your models here.

class Proveedores(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_descuento = models.DateField(null=True, blank=True)
    tipo_descuento = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre
    

class Descuentos(models.Model):
    id_descuento = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedores, to_field='id_proveedor', on_delete=models.CASCADE)
    codigo_qr = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='descuentos_fotos/', null=True, blank=True)

    def __str__(self):
        return f"Descuento {self.id_descuento} - {self.proveedor.nombre}"


class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    socio = models.ForeignKey('Socios', on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id_pago}"

class Socios(models.Model):
    id_socio = models.AutoField(primary_key=True)   
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class Cuotas(models.Model):
    id_cuota = models.AutoField(primary_key=True)
    id_pago = models.ForeignKey(Pagos, on_delete=models.CASCADE, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Cuota {self.id_cuota} - Pago {self.id_pago.id_pago}"

class Credenciales(models.Model):
    id_credencial = models.AutoField(primary_key=True)
    id_socio = models.OneToOneField(Socios, on_delete=models.CASCADE)
    codigo_qr = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.codigo_qr

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    id_socio = models.OneToOneField(Socios, on_delete=models.CASCADE)
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, null=True, blank=True)
    run = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    passwd = models.CharField(max_length=128)  # Almacenar contraseñas de forma segura

    def __str__(self):
        return self.nombre