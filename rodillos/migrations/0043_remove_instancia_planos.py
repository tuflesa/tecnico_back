# Generated by Django 3.1.7 on 2024-09-24 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0042_bancada_espesores'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instancia',
            name='planos',
        ),
    ]
