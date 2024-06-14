import pytest
from django.test import TestCase, Client
from django.urls import reverse

from PlantCare.forms import AddSoilForm, AddMyPlantForm, AddFertilizationForm
from PlantCare.models import PlantType, Soil, MyPlant, Fertilization


#test czy widok zwraca oczekiwane obiekty PlantType
@pytest.mark.django_db
def test_show_type_plant(plant_species):
    url = reverse('plant_type_list')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['plant_types'].count() == len(plant_species)
    for p in plant_species:
        assert p in response.context['plant_types']

#test dodawania gatunku rośliny AddPlantTypeView
def test_add_plant_type_get(): #dla użytkownika niezalogowanego
    url = reverse('add_plant_type')
    client = Client()
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f"{login_url}?next={url}"
@pytest.mark.django_db
def test_add_plant_type_get_login(user): #dla użytkownika zalogowanego
    url = reverse('add_plant_type')
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
@pytest.mark.django_db
def test_add_plant_type_post(user):
    url = reverse('add_plant_type')
    client = Client()
    client.force_login(user)
    data = {'species': 'species test'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert PlantType.objects.get(species='species test')


#test czy widok zwraca oczekiwane obiekty MyPlant
@pytest.mark.django_db
def test_show_my_plant(my_plants):
    url = reverse('show_my_plant')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['my_plant'].count() == len(my_plants)
    for mp in my_plants:
        assert mp in response.context['my_plant']

#test na dodawanie rośliny AddMyPlant
# @pytest.mark.django_db
def test_add_my_plant_get(): #dla użytkownika niezalogowanego
    url = reverse('add_my_plant')
    client = Client()
    response = client.get(url)
    login_url = reverse('login')
    assert response.status_code == 302
    assert response.url == f"{login_url}?next={url}"

@pytest.mark.django_db
def test_add_my_plant_get_login(user): #dla uzytkownika zalogowanego
    url = reverse('add_my_plant')
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddMyPlantForm)
@pytest.mark.django_db
def test_add_my_plant_post(plant_type, user):
    url = reverse('add_my_plant')
    client = Client()
    client.force_login(user)
    data = {'name': 'test name',
            'species': plant_type.id,
            'light_requirements': 1,
            'soil_humidity': 1,
            'description': 'test description',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert MyPlant.objects.get(name='test name', species=plant_type.id, light_requirements=1, soil_humidity=1,
                               description='test description')

#test czy widok dla Soil zwraca oczekiwane obiekty:
@pytest.mark.django_db
def test_show_soil(soil):
    url = reverse('show_soil')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['soil'].count() == len(soil)
    for s in soil:
        assert s in response.context['soil']

#test dla dodawania rodzaju podłoża
def test_add_soil_get(): #dla użytkownika niezalogowanego
    url = reverse('add_soil')
    client = Client()
    response = client.get(url)
    login_url = reverse('login')
    assert response.url == f"{login_url}?next={url}"
    assert response.status_code == 302

@pytest.mark.django_db
def test_add_soil_get_login(user): #dla użytkownika zalogowanego
    url = reverse('add_soil')
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddSoilForm) #sprawdzam czy faktycznie wysyłam ten formularz
@pytest.mark.django_db
def test_add_soil_post(user):
    url = reverse('add_soil')
    client = Client()
    client.force_login(user)
    data = {
        'soil_type': 'test soil',
        'soil_manufacturer': 'test manufacturer',
        'comment': 'test comment'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Soil.objects.get(soil_type='test soil', soil_manufacturer='test manufacturer', comment='test comment')


#test czy widok dla Fertilization zwraca oczekiwane obiekty
@pytest.mark.django_db
def test_show_fertilization(fertilization):
    url = reverse('show_fertilization')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['fertilization'].count() == len(fertilization)
    for f in fertilization:
        assert f in response.context['fertilization']

#test dla dodawania AddFertilization

def test_add_fertilization_get(): #dla użytkownika niezalogowanego
    url = reverse('add_fertilization')
    client = Client()
    response = client.get(url)
    login_url = reverse('login')
    assert response.url == f"{login_url}?next={url}"
    assert response.status_code == 302

@pytest.mark.django_db
def test_add_fertilization_get_login(user): #dla użytkownika zalogowanego
    url = reverse('add_fertilization')
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddFertilizationForm)

@pytest.mark.django_db
def test_add_fertilization_post(my_plant, user):
    url = reverse('add_fertilization')
    client = Client()
    client.force_login(user)
    data = {
        'name': 'test name',
        'plant': my_plant.id,
        'date': '2023-01-01',
        'amount': 1
            }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Fertilization.objects.get(name='test name', plant=my_plant.id, date='2023-01-01', amount=1)
