# Generated by Django 4.0.4 on 2022-06-02 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0063_pedido_observaciones2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineaadicional',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='lineaadicional',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='lineapedido',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='lineapedido',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
