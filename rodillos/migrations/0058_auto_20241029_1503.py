# Generated by Django 3.1.7 on 2024-10-29 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0057_rectificacion_fecha_estimada'),
    ]

    operations = [
        migrations.AddField(
            model_name='instancia',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='programa'),
        ),
        migrations.AddField(
            model_name='linearectificacion',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='programa'),
        ),
    ]
