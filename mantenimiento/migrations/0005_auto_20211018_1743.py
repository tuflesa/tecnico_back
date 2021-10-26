# Generated by Django 3.1.7 on 2021-10-18 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estructura', '0001_initial'),
        ('mantenimiento', '0004_auto_20211018_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='numero',
            field=models.CharField(blank=True, default=None, max_length=12, null=True),
        ),
        migrations.CreateModel(
            name='ContadorNotificaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('contador', models.IntegerField(default=0)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estructura.empresa')),
            ],
        ),
    ]