# Generated by Django 3.1.7 on 2022-03-10 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mantenimiento', '0024_auto_20220309_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partetrabajo',
            name='creado_por',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
