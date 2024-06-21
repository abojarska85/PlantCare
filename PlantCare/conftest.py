import pytest
from django.contrib.auth.models import User
from PlantCare.models import PlantType, MyPlant, Soil, Replanting, Fertilization, Watering


@pytest.fixture
def plant_species():
    lst = []
    for i in range(5):
        lst.append(PlantType.objects.create(species=i))
    return lst


@pytest.fixture
def plant_type():
    return PlantType.objects.create(species='test species')


@pytest.fixture
def my_plants(plant_species):
    lst = []
    for i, species in enumerate(plant_species):
        lst.append(MyPlant.objects.create(name=i, species=species, light_requirements=1, soil_humidity=1, description=i))
    return lst


@pytest.fixture
def my_plant(plant_type):
    return MyPlant.objects.create(name='test plant', species=plant_type, light_requirements=1, soil_humidity=1, description='test plant' )


@pytest.fixture
def soils():
    lst = []
    for i in range(5):
        lst.append(Soil.objects.create(soil_type='type', soil_manufacturer='manufacturer', comment='comment'))
    return lst


@pytest.fixture
def replanting(my_plant, soil):
    lst = []
    for i in range(5):
        lst.append(Replanting.objects.create(plant=my_plant, old_soil_type=soil, new_soil_type=soil, date='2023-01-01', comment='comment'))
    return lst


@pytest.fixture
def watering(my_plant, user):
    lst = []
    for i in range(5):
        lst.append(Watering.objects.create(plant=my_plant, water_content=1.0, date='2023-01-01', water_amount=1.0, user=user))
    return lst


@pytest.fixture
def fertilization(my_plant):
    lst = []
    for i in range(5):
        lst.append(Fertilization.objects.create(name='name', plant=my_plant, date='2023-01-01', amount=1))
    return lst


@pytest.fixture
def user():
    return User.objects.create_user(username='test')

@pytest.fixture
def soil():
    return Soil.objects.create(soil_type='test type', soil_manufacturer='test', comment='test soil')
