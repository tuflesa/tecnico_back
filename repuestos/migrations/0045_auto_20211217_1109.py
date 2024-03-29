# Generated by Django 3.1.7 on 2021-12-17 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repuestos', '0044_auto_20211202_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Salida almacén', max_length=100)),
                ('fecha_creacion', models.DateField(default=django.utils.timezone.now)),
                ('responsable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LineaSalida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('almacen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repuestos.almacen')),
                ('repuesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repuestos.repuesto')),
                ('salida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repuestos.salida')),
            ],
        ),
        migrations.AddField(
            model_name='movimiento',
            name='linea_salida',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repuestos.lineasalida'),
        ),
    ]
