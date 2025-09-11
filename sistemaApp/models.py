from django.db import models

# Create your models here.

class Proveedores(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nombre
    

class Descuentos(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo

class Pagos(models.Model):
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    descuento = models.ForeignKey(Descuentos, on_delete=models.CASCADE)
    socio = models.ForeignKey('Socios', on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id} - {self.proveedor.nombre}"
    
class Socios(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Cuotas(models.Model):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Cuota {self.id} - {self.socio.nombre}"