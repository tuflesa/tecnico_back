# Generated by Django 3.1.7 on 2023-11-16 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0106_auto_20231115_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='condicion_pago',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
