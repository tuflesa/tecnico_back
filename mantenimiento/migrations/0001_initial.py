# Generated by Django 3.1.7 on 2021-10-01 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estructura', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoPeriodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoTarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('periodo', models.IntegerField()),
                ('prioridad', models.IntegerField(default=50)),
                ('observaciones', models.TextField()),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estructura.equipo')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mantenimiento.especialidad')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mantenimiento.tipotarea')),
                ('tipo_periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mantenimiento.tipoperiodo')),
            ],
        ),
        migrations.CreateModel(
            name='ParteTrabajo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('finalizado', models.BooleanField(default=False)),
                ('observaciones', models.TextField()),
                ('creada_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partes_creados', to=settings.AUTH_USER_MODEL)),
                ('responsable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partes_responsable', to=settings.AUTH_USER_MODEL)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mantenimiento.tipotarea')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('que', models.TextField(max_length=250)),
                ('cuando', models.TextField(max_length=150)),
                ('donde', models.TextField(max_length=150)),
                ('como', models.TextField(max_length=250)),
                ('cuanto', models.TextField(max_length=150)),
                ('porque', models.TextField(max_length=250)),
                ('quien', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LineaParteTrabajo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('responsables', models.ManyToManyField(related_name='lineas_parte_trabajo', to=settings.AUTH_USER_MODEL)),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mantenimiento.tarea')),
            ],
        ),
    ]
