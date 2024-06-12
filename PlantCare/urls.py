"""
URL configuration for djangoProject_plants project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from PlantCare import views

urlpatterns = [
    path('add_plant_type/', views.AddPlantTypeView.as_view(), name='add_plant_type'),
    path('plant_type_list/', views.ShowPlantTypeView.as_view(), name='plant_type_list'),
    path('add_my_plant/', views.AddMyPlantView.as_view(), name='add_my_plant'),
    path('update_my_plant/<int:pk>/', views.UpdateMyPlantView.as_view(), name='update_my_plant'),
    path('show_my_plant/', views.ShowMyPlantView.as_view(), name='show_my_plant'),
    path('search_plant/', views.SearchPlantsView.as_view(), name='search_plant'),
    path('add_soil/', views.AddSoilView.as_view(), name='add_soil'),
    path('show_soil/', views.ShowSoilView.as_view(), name='show_soil'),
    path('delete_soil/<int:pk>/', views.DeleteSoilView.as_view(), name='delete_soil'),
    path('add_replanting/', views.AddReplantingView.as_view(), name='add_replanting'),
    path('show_replanting/', views.ShowReplantingView.as_view(), name='show_replanting'),
    path('add_watering/', views.AddWateringView.as_view(), name='add_watering'),
    path('show_watering/', views.ShowWateringView.as_view(), name='show_watering'),
    path('add_fertilization/', views.AddFertilizationView.as_view(), name='add_fertilization'),
    path('show_fertilization/', views.ShowFertilizationView.as_view(), name='show_fertilization'),
]
