# Generated by Django 3.1.7 on 2024-08-29 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0110_auto_20240731_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='intervencion',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='revisado',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]