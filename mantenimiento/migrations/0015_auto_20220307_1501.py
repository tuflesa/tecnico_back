# Generated by Django 3.1.7 on 2022-03-07 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0014_auto_20220307_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partetrabajo',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
    ]
