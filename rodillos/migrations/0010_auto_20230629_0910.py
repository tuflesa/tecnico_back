# Generated by Django 3.1.7 on 2023-06-29 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0009_auto_20230613_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elemento',
            name='conjunto',
        ),
        migrations.RemoveField(
            model_name='elemento',
            name='posicion',
        ),
        migrations.RemoveField(
            model_name='elemento',
            name='rodillo',
        ),
        migrations.RemoveField(
            model_name='grupo',
            name='conjuntos',
        ),
        migrations.RemoveField(
            model_name='grupo',
            name='maquina',
        ),
        migrations.RemoveField(
            model_name='montaje',
            name='conjuntos',
        ),
        migrations.RemoveField(
            model_name='montaje',
            name='grupo',
        ),
        migrations.RemoveField(
            model_name='montaje',
            name='maquina',
        ),
        migrations.RemoveField(
            model_name='posicion',
            name='operacion',
        ),
        migrations.RemoveField(
            model_name='rodillo',
            name='posicion',
        ),
        migrations.AddField(
            model_name='rodillo',
            name='operacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rodillos', to='rodillos.operacion'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Conjunto',
        ),
        migrations.DeleteModel(
            name='Elemento',
        ),
        migrations.DeleteModel(
            name='Grupo',
        ),
        migrations.DeleteModel(
            name='Montaje',
        ),
        migrations.DeleteModel(
            name='Posicion',
        ),
    ]
