# Generated by Django 3.1.7 on 2022-03-02 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0009_auto_20220301_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='pendiente',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='partetrabajo',
            name='tareas',
            field=models.ManyToManyField(blank=True, null=True, related_name='lineaparte', to='mantenimiento.Tarea'),
        ),
    ]
