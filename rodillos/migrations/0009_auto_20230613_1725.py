# Generated by Django 3.1.7 on 2023-06-13 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0008_auto_20230613_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='tubo_madre',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
