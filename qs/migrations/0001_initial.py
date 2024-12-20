# Generated by Django 3.1.7 on 2024-12-20 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rodillos', '0074_rodillo_rectificado_por_parejas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acabado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('dim1', models.CharField(max_length=5)),
                ('dim2', models.CharField(max_length=5)),
                ('espesor', models.CharField(max_length=4)),
                ('acabado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qs.acabado')),
            ],
        ),
        migrations.CreateModel(
            name='Calidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Formas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Norma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Variante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('pr_inf', models.FloatField()),
                ('pr_presion', models.FloatField()),
                ('bd1_sup', models.FloatField()),
                ('bd1_inf', models.FloatField()),
                ('bd2_sup', models.FloatField()),
                ('bd2_inf', models.FloatField()),
                ('is1_ancho', models.FloatField()),
                ('is1_alto', models.FloatField()),
                ('l_entrada_sup', models.FloatField()),
                ('l_entrada_ancho', models.FloatField()),
                ('l_entrada_alto', models.FloatField()),
                ('l_entrada_rod_inf', models.FloatField()),
                ('l_centro_rod_inf', models.FloatField()),
                ('l_saluda_sup', models.FloatField()),
                ('l_salida_ancho', models.FloatField()),
                ('l_salida_alto', models.FloatField()),
                ('l_salida_rod_inf', models.FloatField()),
                ('fp1_sup', models.FloatField()),
                ('fp1_inf', models.FloatField()),
                ('is2_ancho', models.FloatField()),
                ('is2_alto', models.FloatField()),
                ('fp2_sup', models.FloatField()),
                ('fp2_inf', models.FloatField()),
                ('is3_ancho', models.FloatField()),
                ('is3_alto', models.FloatField()),
                ('fp3_sup', models.FloatField()),
                ('fp3_inf', models.FloatField()),
                ('w_inf', models.FloatField()),
                ('w_lat_op', models.FloatField()),
                ('w_lat_mo', models.FloatField()),
                ('w_sup_op_v', models.FloatField()),
                ('w_sup_op_h', models.FloatField()),
                ('w_sup_mo_v', models.FloatField()),
                ('w_sup_mo_h', models.FloatField()),
                ('cb1_sup', models.FloatField()),
                ('cb1_inf', models.FloatField()),
                ('cb1_lat_op', models.FloatField()),
                ('cb1_lat_mo', models.FloatField()),
                ('cb2_sup', models.FloatField()),
                ('cb2_inf', models.FloatField()),
                ('cb2_lat_op', models.FloatField()),
                ('cb2_lat_mo', models.FloatField()),
                ('cb3_sup', models.FloatField()),
                ('cb3_inf', models.FloatField()),
                ('cb3_lat_op', models.FloatField()),
                ('cb3_lat_mo', models.FloatField()),
                ('cb4_sup', models.FloatField()),
                ('cb4_inf', models.FloatField()),
                ('cb4_lat_op', models.FloatField()),
                ('cb4_lat_mo', models.FloatField()),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qs.articulo')),
                ('montaje', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rodillos.montaje')),
            ],
        ),
        migrations.AddField(
            model_name='articulo',
            name='calidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qs.calidad'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='forma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qs.formas'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='montajes',
            field=models.ManyToManyField(related_name='articulos', to='rodillos.Montaje'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='norma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qs.norma'),
        ),
    ]
