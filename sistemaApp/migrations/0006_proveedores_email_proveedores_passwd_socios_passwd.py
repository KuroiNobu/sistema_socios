from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistemaApp', '0005_usuarios_tipo_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedores',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='proveedores',
            name='passwd',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='socios',
            name='passwd',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
