# Generated by Django 3.1.7 on 2021-10-18 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estructura', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mantenimiento', '0003_auto_20211006_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='empresa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='estructura.empresa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notificacion',
            name='finalizado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='para',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificaciones_recividas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='revisado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notificacion',
            name='quien',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificaciones_enviadas', to=settings.AUTH_USER_MODEL),
        ),
    ]