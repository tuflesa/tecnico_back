# Generated by Django 3.1.7 on 2021-05-10 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargas', '0002_auto_20210508_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='carga',
            name='telefono',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]