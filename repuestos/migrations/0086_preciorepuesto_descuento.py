# Generated by Django 4.0.4 on 2022-11-18 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0085_alter_lineaadicional_total_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='preciorepuesto',
            name='descuento',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]