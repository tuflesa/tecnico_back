# Generated by Django 3.1.7 on 2025-05-26 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trazabilidad', '0008_auto_20250526_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='acumulador',
            name='db',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acumulador',
            name='ip',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='acumulador',
            name='rack',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='acumulador',
            name='slot',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
