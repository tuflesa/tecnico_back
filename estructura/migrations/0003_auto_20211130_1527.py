# Generated by Django 3.1.7 on 2021-11-30 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estructura', '0002_auto_20211126_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='logo',
            field=models.ImageField(null=True, upload_to='logos'),
        ),
        migrations.CreateModel(
            name='Direcciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(blank=True, max_length=20, null=True)),
                ('poblacion', models.CharField(blank=True, max_length=10, null=True)),
                ('codpostal', models.CharField(blank=True, max_length=5, null=True)),
                ('telefono', models.CharField(blank=True, max_length=9, null=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estructura.empresa')),
            ],
        ),
    ]
