# Generated by Django 3.1.7 on 2021-10-06 09:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partetrabajo',
            name='finalizado',
        ),
        migrations.AddField(
            model_name='lineapartetrabajo',
            name='parte',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lineas', to='mantenimiento.partetrabajo'),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='conclusion',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='descartado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='fecha_creacion',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='partetrabajo',
            name='notificacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partes', to='mantenimiento.notificacion'),
        ),
    ]