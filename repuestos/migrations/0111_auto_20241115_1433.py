# Generated by Django 3.1.7 on 2024-11-15 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0110_auto_20240731_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='condicion_pago',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]