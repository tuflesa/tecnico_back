# Generated by Django 3.1.7 on 2024-11-27 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0066_auto_20241121_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='linearectificacion',
            name='diametro_centro',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='linearectificacion',
            name='nuevo_diametro_centro',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
