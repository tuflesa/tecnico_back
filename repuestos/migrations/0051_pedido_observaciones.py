# Generated by Django 3.1.7 on 2022-01-18 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0050_repuesto_observaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='observaciones',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
