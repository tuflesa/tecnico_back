# Generated by Django 3.1.7 on 2024-07-31 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0109_auto_20240109_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='intervencion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pedido',
            name='revisado',
            field=models.BooleanField(default=False),
        ),
    ]