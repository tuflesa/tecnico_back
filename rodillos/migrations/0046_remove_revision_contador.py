# Generated by Django 3.1.7 on 2024-09-25 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rodillos', '0045_revision_contador'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revision',
            name='contador',
        ),
    ]