# Generated by Django 3.1.7 on 2024-11-19 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0109_auto_20240109_0722'),
        ('rodillos', '0062_auto_20241118_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='linearectificacion',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repuestos.proveedor'),
        ),
    ]
