import pytest
from django.test import TestCase, Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from PlantCare.forms import AddSoilForm, AddMyPlantForm, AddFertilizationForm, AddWateringForm, AddReplantingForm, \
    SearchForm
from PlantCare.models import PlantType, Soil, MyPlant, Fertilization, Watering, Replanting


#model PlantType
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



#model MyPlant
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
    assert MyPlant.objects.get(name='test name', species=plant_type, light_requirements=1, soil_humidity=1,
                               description='test description')


#test dla wyszukiwania rośliny
@pytest.mark.django_db
def test_search_plants_view(): #sprawdzenie czy widok jest dostępny i czy w kontekście jest formularz
    url = reverse('search_plant')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], SearchForm)

#test dla widoku UpdateMyPlant:
@pytest.mark.django_db
def test_update_my_plant_get(my_plant): #dla niezalogowanego użytkownika
    url = reverse('update_my_plant', args=[my_plant.pk])
    client = Client()
    response = client.get(url)
    login_url = reverse('login')
    assert response.status_code == 302
    assert response.url == f"{login_url}?next={url}"
@pytest.mark.django_db
def test_update_my_plant_get_login(user, my_plant): #dla zalogowanego uzytkownika, formularz w kontekście
    url = reverse('update_my_plant', args=[my_plant.pk])
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddMyPlantForm)


@pytest.mark.django_db
def test_update_my_plant_post(my_plant, user, plant_type): #sprawdza czy dane zostały zmienione i zapisane
    url = reverse('update_my_plant', args=[my_plant.pk])
    client = Client()
    client.force_login(user)
    data = {
        'name': 'test name',
        'species': plant_type.id,
        'light_requirements': 1,
        'soil_humidity': 1,
        'description': 'test description'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert MyPlant.objects.get(pk=my_plant.pk).name == 'test name'
    assert MyPlant.objects.get(pk=my_plant.pk).species == plant_type
    assert MyPlant.objects.get(pk=my_plant.pk).light_requirements == 1
    assert MyPlant.objects.get(pk=my_plant.pk).soil_humidity == 1
    assert MyPlant.objects.get(pk=my_plant.pk).description == 'test description'



#model Soil
#test czy widok dla Soil zwraca oczekiwane obiekty:
@pytest.mark.django_db
def test_show_soil(soils):
    url = reverse('show_soil')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['soil'].count() == len(soils)
    for s in soils:
        assert s in response.context['soil']


#test dla dodawania rodzaju podłoża AddSoilView
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


#test dla widoku DeleteSoilView
@pytest.mark.django_db
def test_delete_soil_get(soil): #dla użytkownika niezalogowanego
    url = reverse('delete_soil', args=[soil.id])
    client = Client()
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f"{login_url}?next={url}"
@pytest.mark.django_db
def test_delete_soil_get_login(user, soil): #dla użytkownika zalogowanego, kontekst, template
    url = reverse('delete_soil', args=[soil.id])
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['soil'], Soil)
    assertTemplateUsed(response, "plantCare/soil_delete.html")

@pytest.mark.django_db
def test_delete_soil_post_action(user, soil): #test dla usuwania gdy jest zgoda
    url = reverse('delete_soil', args=[soil.id])
    client = Client()
    client.force_login(user)
    data = {'action': 'tak'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('show_soil') #sprawdzam przekierowanie
    with pytest.raises(Soil.DoesNotExist): #sprawdzam czy pobranie obiektu spowoduje wyjątek
        Soil.objects.get(pk=soil.pk)
@pytest.mark.django_db
def test_delete_soil_post_no_action(user, soil):
    url = reverse('delete_soil', args=[soil.id])
    client = Client()
    client.force_login(user)
    data = {'action': 'nie'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert Soil.objects.filter(pk=soil.pk).exists() #sprawdzam że obiekt nadal istnieje w bazie





#model Replanting
#test dodawanie przesadzania do widoku AddReplantingView
@pytest.mark.django_db
def test_show_replanting(my_plants, soils, replanting): #test chodzi, ale w mojej ocenie jest niepełny
    url = reverse('show_replanting')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['replanting'].count() == len(replanting)
    for r in replanting:
        assert r in response.context['replanting']

def test_add_replanting_get(): #dla użytkownika niezalogowanego
    url = reverse('add_replanting')
    client = Client()
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f"{login_url}?next={url}"
@pytest.mark.django_db
def test_add_replanting_get_login(user): #dla użytkownika zalogowanego
    url = reverse('add_replanting')
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddReplantingForm)


@pytest.mark.django_db
def test_add_replanting_post(my_plant, soil, user):
    url = reverse('add_replanting')
    client = Client()
    client.force_login(user)
    data = {
        'plant': my_plant.id,
        'old_soil_type': soil.id,
        'new_soil_type': soil.id,
        'date': '2023-01-01',
        'comment': 'test comment'
        }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Replanting.objects.get(plant=my_plant, old_soil_type=soil, new_soil_type=soil, date='2023-01-01', comment='test comment')


#model Watering
@pytest.mark.django_db
def test_show_watering(my_plants, watering): #test chodzi, ale można by było jeszcze coś dodatkowo przetestowć
    url = reverse('show_watering')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['watering'].count() == len(my_plants)
    for w in watering:
        assert w in response.context['watering']


#test na dodawanie podlewania do widoku AddWateringView
def test_add_watering_get(): #dla użytkownika niezalogowanego
    url = reverse('add_watering')
    client = Client()
    response = client.get(url)
    assert response.status_code == 302
    login_url = reverse('login')
    assert response.url == f"{login_url}?next={url}"


@pytest.mark.django_db
def test_add_watering_get_login(user): #dla użytkownika zalogowanego
    url = reverse('add_watering')
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddWateringForm)


@pytest.mark.django_db
def test_add_watering_post(my_plant, user):
    url = reverse('add_watering')
    client = Client()
    client.force_login(user)
    data = {
        'plant': my_plant.id,
        'water_content': 1.0,
        'date': '2023-01-01',
        'water_amount': 1.0,
        'user': user.id
        }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Watering.objects.get(plant=my_plant.id, water_content=1.0, date='2023-01-01', water_amount=1.0, user=user.id)


#model Fertilization
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
    assert Fertilization.objects.get(name='test name', plant=my_plant, date='2023-01-01', amount=1)
