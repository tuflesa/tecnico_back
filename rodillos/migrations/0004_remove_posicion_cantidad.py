# Generated by Django 3.1.7 on 2023-03-03 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0003_posicion_cantidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posicion',
            name='cantidad',
        ),
    ]
