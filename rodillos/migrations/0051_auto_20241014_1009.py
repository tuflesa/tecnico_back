# Generated by Django 3.1.7 on 2024-10-14 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estructura', '0012_auto_20240823_1347'),
        ('rodillos', '0050_rectificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rectificacion',
            name='numero',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='ContadorRectificaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('contador', models.IntegerField(default=0)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estructura.empresa')),
            ],
        ),
    ]
