from django import forms
from django.utils.html import format_html
from sistemaApp.models import Usuarios, Credenciales, Socios, Pagos, Cuotas, Descuentos, Proveedores, SolicitudIngreso


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'})
    )


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
        labels = {
            'id_usuario': 'ID Usuario',
            'run': 'Run',
            'nombre': 'Nombre',
            'email': 'Email',
            'passwd': 'Contraseña',
        }
        widgets = {
            'id_usuario':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa ID usuario'}),
            'run':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa Run'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa nombre'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingresa email'}),
            'passwd':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Ingresa contraseña'}),
        }

class SociosForm(forms.ModelForm):
    passwd = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa contraseña'}),
        required=False,
    )

    class Meta:
        model = Socios
        exclude = ['id_usuario']
        widgets = {
            'id_socio':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa ID socio'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa nombre'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingresa email'}),
            'telefono':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa telefono'}),
            'fecha_registro':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        }

    def clean_passwd(self):
        password = self.cleaned_data.get('passwd', '')
        if not password:
            if self.instance.pk and self.instance.passwd:
                return self.instance.passwd
            raise forms.ValidationError('Ingresa una contraseña.')
        return password

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
    passwd = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa contraseña'}),
        required=False,
    )

    class Meta:
        model = Proveedores
        exclude = ['id_usuario']
        widgets = {
            'id_proveedor':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa ID proveedor'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa nombre'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingresa email'}),
            'fecha_descuento':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'tipo_descuento':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa tipo descuento'}),
        }

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if not email:
            raise forms.ValidationError('Ingresa un correo electrónico.')
        return email

    def clean_passwd(self):
        password = self.cleaned_data.get('passwd', '')
        if not password:
            if self.instance.pk and self.instance.passwd:
                return self.instance.passwd
            raise forms.ValidationError('Ingresa una contraseña.')
        return password

class CredencialesForm(forms.ModelForm):
    class Meta:
        model = Credenciales
        fields = '__all__'
        widgets = {
                'id_credencial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa ID credencial'}),
                'id_socio': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Selecciona socio'}),
                'codigo_qr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa codigo QR'}),
            }


class SocioPerfilForm(forms.ModelForm):
    passwd = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nueva contraseña'}),
        required=False,
    )

    class Meta:
        model = Socios
        fields = ['nombre', 'apellido', 'email', 'telefono', 'passwd']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu teléfono'}),
        }

    def save(self, usuario=None, commit=True):
        socio = super().save(commit=False)
        new_password = self.cleaned_data.get('passwd')
        if usuario is not None:
            socio.id_usuario = usuario
        if new_password:
            socio.passwd = new_password
        if commit:
            socio.save()
        return socio

    def clean_passwd(self):
        password = self.cleaned_data.get('passwd', '')
        if not password:
            if not self.instance.pk or not getattr(self.instance, 'passwd', ''):
                raise forms.ValidationError('Ingresa una contraseña para tu cuenta de socio.')
            return self.instance.passwd
        return password


class SolicitudIngresoForm(forms.ModelForm):
    class Meta:
        model = SolicitudIngreso
        fields = ['tipo', 'nombre', 'apellido', 'email', 'telefono', 'comentarios']
        labels = {
            'tipo': 'Quiero ser',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono de contacto',
            'comentarios': 'Comentarios adicionales',
        }
        widgets = {
            'tipo': forms.RadioSelect(choices=SolicitudIngreso.TIPO_CHOICES, attrs={'class': 'solicitud-radios'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu apellido (opcional)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu teléfono (opcional)'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Cuéntanos por qué quieres unirte', 'rows': 3}),
        }


class FiltroSociosForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o apellido'}),
    )
    email = forms.CharField(
        label='Correo',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correo de socio'}),
    )
    telefono = forms.CharField(
        label='Teléfono',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
    )
    fecha_inicio = forms.DateField(
        label='Registrado desde',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    fecha_fin = forms.DateField(
        label='Registrado hasta',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fecha_inicio')
        fin = cleaned_data.get('fecha_fin')
        if inicio and fin and inicio > fin:
            raise forms.ValidationError('La fecha de inicio no puede ser posterior a la fecha de término.')
        return cleaned_data
