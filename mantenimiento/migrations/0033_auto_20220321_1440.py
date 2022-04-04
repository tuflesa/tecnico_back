# Generated by Django 3.1.7 on 2022-03-21 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0032_estadolineastareas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineapartetrabajo',
            name='finalizada',
        ),
        migrations.AddField(
            model_name='lineapartetrabajo',
            name='estado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mantenimiento.estadolineastareas'),
        ),
    ]
