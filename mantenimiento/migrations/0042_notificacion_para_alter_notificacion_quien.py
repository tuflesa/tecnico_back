# Generated by Django 4.0.4 on 2022-05-19 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mantenimiento', '0041_alter_notificacion_quien'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='para',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificaciones_recividas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notificacion',
            name='quien',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificaciones_enviadas', to=settings.AUTH_USER_MODEL),
        ),
    ]
