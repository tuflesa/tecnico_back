# Generated by Django 3.1.7 on 2023-11-07 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estructura', '0007_auto_20220117_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='direcciones',
            name='cif',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]