# Generated by Django 3.1.7 on 2023-10-03 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0021_auto_20230928_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('valor', models.FloatField()),
                ('revision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rodillos.revision')),
            ],
        ),
    ]
