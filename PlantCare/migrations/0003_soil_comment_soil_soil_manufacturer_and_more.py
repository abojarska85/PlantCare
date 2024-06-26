# Generated by Django 5.0.6 on 2024-06-11 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlantCare', '0002_rename_plant_genre_myplant_species_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='soil',
            name='comment',
            field=models.TextField(default='no comment', null=True),
        ),
        migrations.AddField(
            model_name='soil',
            name='soil_manufacturer',
            field=models.CharField(default='Default Manufacturer', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='replanting',
            name='new_soil_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_soil_type', to='PlantCare.soil'),
        ),
        migrations.AlterField(
            model_name='replanting',
            name='old_soil_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='old_soil_type', to='PlantCare.soil'),
        ),
        migrations.AlterField(
            model_name='soil',
            name='soil_type',
            field=models.CharField(max_length=250),
        ),
    ]
