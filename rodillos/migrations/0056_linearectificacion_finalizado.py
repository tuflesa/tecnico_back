# Generated by Django 3.1.7 on 2024-10-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0055_rectificacion_finalizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='linearectificacion',
            name='finalizado',
            field=models.BooleanField(default=False),
        ),
    ]