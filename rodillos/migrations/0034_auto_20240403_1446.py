# Generated by Django 3.1.7 on 2024-04-03 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0033_celda_operacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celda',
            name='operacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rodillos.operacion'),
        ),
    ]
