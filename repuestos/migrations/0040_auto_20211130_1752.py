# Generated by Django 3.1.7 on 2021-11-30 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0039_auto_20211130_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='direccion_entrega',
            new_name='direccion_envio',
        ),
    ]