# Generated by Django 3.1.7 on 2023-11-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0100_proveedor_poblacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='condicion_entrega',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='condicion_pago',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
