# Generated by Django 3.1.7 on 2023-12-05 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0107_auto_20231116_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='descripcion',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='observaciones',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='observaciones2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
