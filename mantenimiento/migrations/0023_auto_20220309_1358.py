# Generated by Django 3.1.7 on 2022-03-09 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mantenimiento', '0022_auto_20220309_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partetrabajo',
            name='creada_por',
        ),
        migrations.AddField(
            model_name='partetrabajo',
            name='creado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
