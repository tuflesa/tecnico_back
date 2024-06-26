# Generated by Django 3.1.7 on 2023-10-25 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0023_auto_20231024_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='conjunto',
            name='tubo_madre',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='operacion',
            name='orden',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rodillo',
            name='diametro',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seccion',
            name='orden',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
