# Generated by Django 3.1.7 on 2024-12-03 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0068_plano_xa_rectificado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rodillo',
            name='tipo_plano',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rodillos.tipo_plano'),
        ),
    ]