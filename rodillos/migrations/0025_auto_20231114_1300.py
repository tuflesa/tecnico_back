# Generated by Django 3.1.7 on 2023-11-14 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0024_auto_20231025_0759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bancada',
            name='grupos',
        ),
        migrations.AddField(
            model_name='bancada',
            name='tubo_madre',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grupo',
            name='bancadas',
            field=models.ManyToManyField(related_name='grupos', to='rodillos.Bancada'),
        ),
    ]