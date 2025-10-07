from django import forms
from django.utils.html import format_html
from sistemaApp.models import Usuarios, Credenciales, Socios, Pagos, Cuotas, Descuentos, Proveedores

class verLogo(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs, **kwargs)
        img_html = ''
        if value and hasattr(value, 'url'):
            img_html = format_html(f'<br><img src="{value.url}" width="100" class="mb-2"/>')
        return format_html(f'{img_html}{input_html}')

class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = '__all__'
        widgets = {
            'id_usuario':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa ID usuario'}),
            'run':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa Run'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa nombre'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingresa email'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Ingresa password'}),
        }

class SociosForm(forms.ModelForm):
    class Meta:
        model = Socios
        fields = '__all__'
        widgets = {
            'id_socio':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa ID socio'}),
            'id_usuario':forms.Select(attrs={'class':'form-select','placeholder':'Selecciona usuario'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa nombre'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingresa email'}),
            'telefono':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa telefono'}),
            'fecha_registro':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        }

class PagosForm(forms.ModelForm):
    class Meta:
        model = Pagos
        fields = '__all__'
        widgets = {
            'id_pago':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa ID pago'}),
            'id_socio':forms.Select(attrs={'class':'form-select','placeholder':'Selecciona socio'}),
            'monto':forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingresa monto'}),
            'fecha_pago':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        }

class CuotasForm(forms.ModelForm):
    class Meta:
        model = Cuotas
        fields = '__all__'
        widgets = {
            'id_cuota':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa ID cuota'}),
            'id_pago':forms.Select(attrs={'class':'form-select','placeholder':'Selecciona pago'}),
            'monto':forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingresa monto'}),
            'fecha_vencimiento':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'pagado':forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }  

class DescuentosForm(forms.ModelForm):
    class Meta:
        model = Descuentos
        fields = '__all__'
        widgets = {
            'id_descuento':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa ID descuento'}),
            'id_proveedor':forms.Select(attrs={'class':'form-select','placeholder':'Selecciona proveedor'}),
            'codigo_qr':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa codigo QR'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','placeholder':'Ingresa descripcion','rows':3}),
            'foto': verLogo(attrs={'class': 'form-control', 'placeholder': 'Selecciona foto'}),
        }

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields = '__all__'
        widgets = {
            'id_proveedor':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa ID proveedor'}),
            'id_usuario':forms.Select(attrs={'class':'form-select','placeholder':'Selecciona usuario'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa nombre'}),
            'fecha_descuento':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'tipo_descuento':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa tipo descuento'}),
        }

class CredencialesForm(forms.ModelForm):
    class Meta:
        model = Credenciales
        fields = '__all__'
        widgets = {
                'id_credencial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa ID credencial'}),
                'id_socio': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Selecciona socio'}),
                'codigo_qr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa codigo QR'}),
            }
