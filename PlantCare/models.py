import datetime

from django.contrib.auth.models import User
from django.db import models


class PlantType(models.Model):
    species = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.species}"


class MyPlant(models.Model):
    name = models.CharField(max_length=250, verbose_name="nazwa rośliny")
    species = models.ForeignKey(PlantType, on_delete=models.CASCADE, verbose_name="gatunek")
    light_req_types = (
        (1, 'bardzo jasne'),
        (2, 'jasne, światło rozproszone'),
        (3, 'półcieniste'),
        (4, 'cieniste')
    )
    light_requirements = models.IntegerField(choices=light_req_types, default=None, verbose_name="warunki świetlne")
    soil_humidity_types = (
        (1, 'długo utrzymujące wilgoć'),
        (2, 'przepuszczalne'),
        (3, 'wysoko przepuszczalne')
    )
    soil_humidity = models.IntegerField(choices=soil_humidity_types, default=None, verbose_name="przepuszczalność podłoża")
    description = models.TextField(verbose_name="uwagi")

    def __str__(self):
        return f"{self.name}"


class Soil(models.Model):
    soil_type = models.CharField(max_length=250, verbose_name="rodzaj podłoża")
    soil_manufacturer = models.CharField(max_length=250, default="Default Manufacturer", null=True, verbose_name='producent')
    comment = models.TextField(default='no comment', null=True, verbose_name="uwagi")

    def __str__(self):
        return f"{self.soil_type}"


class Replanting(models.Model):
    plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE, verbose_name="roślina")
    old_soil_type = models.ForeignKey(Soil, on_delete=models.CASCADE, related_name='old_soil_type', verbose_name="wymieniane podłoże")
    new_soil_type = models.ForeignKey(Soil, on_delete=models.CASCADE, related_name='new_soil_type', verbose_name='nowe podłoże')
    date = models.DateField(default=datetime.date.today, verbose_name='data')
    comment = models.TextField()


    def __str__(self):
        return f"{self.plant}, {self.date}, {self.comment}"


class Watering(models.Model):
    plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE, verbose_name='roślina', help_text="Wybierz roślinę do podlewania")
    water_content = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='pomiar wilgotności podłoża', help_text="Sprawdź za pomocą higrometru wilgotność gleby")
    date = models.DateField(default=datetime.date.today, verbose_name='data')
    water_amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='ilość wody w ml', help_text="Podaj ilość wlanej wody w ml")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name="użytkownik")
    # wyświetlić procedurę podlewania przy każdym podlewaniu


class Fertilization(models.Model):
    name = models.CharField(max_length=250, verbose_name='nazwa nawozu')
    plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE, verbose_name='roślina')
    date = models.DateField(default=datetime.date.today, verbose_name='data')
    amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='dawka (ml)')

    def __str__(self):
        return f"{self.name}, {self.plant}, {self.date}, {self.amount}"

# class PlantImages(models.Model):
#     image = models.ImageField(upload_to='plant_images/')
#     plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE)

# model dodatkowy jak starczy mi czasu
# class Caretaking(models.Model):
#     plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE)
#     date = models.DateField(default=datetime.date.today)
#     care_type = models.CharField(max_length=250)
#     care_description = models.TextField()
#     reproduction = models.BooleanField(default=False)
#     reproduction_description = models.TextField()
