# Generated by Django 3.1.7 on 2022-03-01 13:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0008_partetrabajo_finalizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='partetrabajo',
            name='fecha_creacion',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='partetrabajo',
            name='fecha_finalizacion',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='partetrabajo',
            name='tareas',
            field=models.ManyToManyField(related_name='lineaparte', to='mantenimiento.Tarea'),
        ),
    ]
