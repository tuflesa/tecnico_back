# Generated by Django 3.1.7 on 2023-11-08 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0103_remove_proveedor_iva'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='pais',
            field=models.TextField(default='España', max_length=75),
        ),
    ]
