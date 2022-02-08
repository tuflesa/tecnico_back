# Generated by Django 3.1.7 on 2022-02-07 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0053_remove_movimiento_stock_resultante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineasalida',
            name='almacen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineas', to='repuestos.almacen'),
        ),
        migrations.AlterField(
            model_name='lineasalida',
            name='repuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineas', to='repuestos.repuesto'),
        ),
        migrations.AlterField(
            model_name='lineasalida',
            name='salida',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='lineas', to='repuestos.salida'),
        ),
    ]
