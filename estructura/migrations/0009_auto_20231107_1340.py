# Generated by Django 3.1.7 on 2023-11-07 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estructura', '0008_direcciones_cif'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='cif',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='codpostal',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='direccion',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='poblacion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
