# Generated by Django 3.1.7 on 2024-11-21 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0065_auto_20241121_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rodillo',
            name='dimension_perfil',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
