# Generated by Django 5.0.6 on 2024-06-08 18:04

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyPlant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('light_requirements', models.IntegerField(choices=[(1, 'bardzo jasne'), (2, 'jasne, rozproszone'), (3, 'półcieniste'), (4, 'cieniste')], default='not defined')),
                ('soil_humidity', models.IntegerField(choices=[(1, 'długo utrzymujące wilgoć'), (2, 'przepuszczalne'), (3, 'wysoko przepuszczalne')], default='not defined')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PlantType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Soil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soil_type', models.IntegerField(choices=[(1, 'podłoże dla roślin wilgociolubnych'), (2, 'podłoże uniwersalne'), (3, 'podłoże dla roślin obrazkowatych'), (4, 'podłoże dla epifitów'), (5, 'podłoże dla roślin sucholubnych'), (6, 'podłoże produkcyjne')], default='not defined')),
            ],
        ),
        migrations.CreateModel(
            name='Fertilization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlantCare.myplant')),
            ],
        ),
        migrations.AddField(
            model_name='myplant',
            name='plant_genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlantCare.planttype'),
        ),
        migrations.CreateModel(
            name='Replanting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField()),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlantCare.myplant')),
            ],
        ),
        migrations.CreateModel(
            name='Watering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water_content', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date', models.DateField(default=datetime.date.today)),
                ('water_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlantCare.myplant')),
            ],
        ),
    ]
