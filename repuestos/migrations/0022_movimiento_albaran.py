# Generated by Django 3.1.7 on 2021-10-08 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0021_pedido_finalizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='albaran',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
