# Generated by Django 4.0.4 on 2022-05-25 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0049_remove_partetrabajo_periodo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarea',
            name='trabajo',
        ),
    ]