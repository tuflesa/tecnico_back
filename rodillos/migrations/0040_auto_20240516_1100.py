# Generated by Django 3.1.7 on 2024-05-16 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0039_auto_20240503_1307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operacion',
            old_name='imagen',
            new_name='icono',
        ),
    ]
