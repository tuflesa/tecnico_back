# Generated by Django 3.1.7 on 2025-04-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0087_auto_20250401_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rodillo',
            name='dimension_perfil',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
