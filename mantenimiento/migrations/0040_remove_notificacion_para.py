# Generated by Django 4.0.4 on 2022-05-19 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0039_alter_notificacion_quien'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificacion',
            name='para',
        ),
    ]
