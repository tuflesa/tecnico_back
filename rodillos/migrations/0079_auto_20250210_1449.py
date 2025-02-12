# Generated by Django 3.1.7 on 2025-02-10 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0078_operacion_icono_celda'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bancada',
            options={'ordering': ['seccion__orden', 'id']},
        ),
        migrations.AlterModelOptions(
            name='celda',
            options={'ordering': ['operacion__orden', 'id']},
        ),
        migrations.AlterModelOptions(
            name='montaje',
            options={'ordering': ['grupo__tubo_madre', 'grupo', 'titular_grupo']},
        ),
        migrations.AddField(
            model_name='montaje',
            name='anotciones_montaje',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='montaje',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='anotaciones_montaje'),
        ),
    ]
