# Generated by Django 3.1.7 on 2025-05-22 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0088_auto_20250429_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celda',
            name='conjunto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conjunto_celda', to='rodillos.conjunto'),
        ),
    ]
