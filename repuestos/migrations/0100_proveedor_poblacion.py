# Generated by Django 3.1.7 on 2023-11-07 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0099_auto_20231107_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='poblacion',
            field=models.TextField(blank=True, max_length=75, null=True),
        ),
    ]