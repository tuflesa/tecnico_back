# Generated by Django 3.1.7 on 2022-03-14 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0027_auto_20220314_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partetrabajo',
            name='tarea',
        ),
        migrations.AddField(
            model_name='partetrabajo',
            name='tarea',
            field=models.ManyToManyField(blank=True, null=True, related_name='partes', to='mantenimiento.Tarea'),
        ),
    ]