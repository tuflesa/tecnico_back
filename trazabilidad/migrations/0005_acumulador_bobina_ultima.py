# Generated by Django 3.1.7 on 2025-05-16 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trazabilidad', '0004_acumulador_maquina_siglas'),
    ]

    operations = [
        migrations.AddField(
            model_name='acumulador',
            name='bobina_ultima',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
