# Generated by Django 4.0.4 on 2023-05-17 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0058_alter_notificacion_conclusion'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='peligrosidad',
            field=models.BooleanField(default=False),
        ),
    ]
