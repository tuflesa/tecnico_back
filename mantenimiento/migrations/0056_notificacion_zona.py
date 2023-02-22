# Generated by Django 4.0.4 on 2023-02-16 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estructura', '0007_auto_20220117_1420'),
        ('mantenimiento', '0055_merge_20230110_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='zona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones_creadas', to='estructura.zona'),
        ),
    ]