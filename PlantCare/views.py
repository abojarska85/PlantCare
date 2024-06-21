from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from PlantCare.forms import AddMyPlantForm, AddSoilForm, AddReplantingForm, AddWateringForm, AddFertilizationForm, \
    SearchForm
from PlantCare.labels import light_label, humidity_label
from PlantCare.models import PlantType, MyPlant, Soil, Replanting, Watering, Fertilization


class AddPlantTypeView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'plantCare/add_plant_type.html')

    def post(self, request):
        species = request.POST.get('species')
        PlantType.objects.create(species=species)
        return render(request, 'plantCare/add_plant_type.html', {'species': species})


class ShowPlantTypeView(View):
    def get(self, request):
        plant_types = PlantType.objects.all()
        return render(request, 'plantCare/plant_type.html', {'plant_types': plant_types})


class AddMyPlantView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddMyPlantForm()
        return render(request, 'plantCare/form.html', {'form': form})

    def post(self, request):
        form = AddMyPlantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            species = form.cleaned_data['species']
            light_requirements = form.cleaned_data['light_requirements']
            soil_humidity = form.cleaned_data['soil_humidity']
            description = form.cleaned_data['description']
            MyPlant.objects.create(name=name, species=species, light_requirements=light_requirements,
                                   soil_humidity=soil_humidity, description=description)
            return redirect('add_my_plant')
        return render(request, 'plantCare/form.html', {'form': form})


class ShowMyPlantView(View):
    def get(self, request):
        my_plant = MyPlant.objects.all()
        for plant in my_plant:
            plant.light_requirements = light_label(plant.light_requirements)
            plant.soil_humidity = humidity_label(plant.soil_humidity)
        return render(request, 'plantCare/my_plant.html', {'my_plant': my_plant})


# class SearchPlantsView(View):
#     def get(self, request):
#         search_query = request.GET.get('search_query', "")
#         form = SearchForm(request.GET)
#         results = MyPlant.objects.filter(name__icontains=search_query)
#         return render(request, 'plantCare/search_result.html', {"form": form, "results": results})
#
#     def post(self, request):
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             search_query = form.cleaned_data['search_query']
#             # if search_query:
#             plants = MyPlant.objects.filter(name__icontains=search_query)
#         return render(request, 'plantCare/search_result.html',
#                               {"search_results": plants, "search_text": search_query})
#         # return render(request, 'plantCare/search_result.html', {'form': form})

# class SearchPlantsView(View):
#     template = 'plantCare/search_result.html'
#
#     def get_search_results(self, query):
#         return MyPlant.objects.filter(name__icontains=query)
#
#     def handle_search(self, request):
#         form = SearchForm(request.GET if request.method == 'GET' else request.POST)
#         results = []
#         search_query = ""
#         if form.is_valid():
#             search_query = form.cleaned_data['search_query']
#             results = self.get_search_results(search_query)
#         return render(request, self.template, {'form': form, 'results': results, 'search_query': search_query})
#
#     def get(self, request):
#         return self.handle_search(request)
#
#     def post(self, request):
#         return self.handle_search(request)

class SearchPlantsView(ListView):
    model = MyPlant
    template_name = 'plantCare/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('search_query', '')
        return MyPlant.objects.filter(name__icontains=query)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context


class UpdateMyPlantView(LoginRequiredMixin, View):
    def get(self, request, pk):
        my_plant = MyPlant.objects.get(pk=pk)
        form = AddMyPlantForm(instance=my_plant)
        return render(request, 'plantCare/form.html', {'form': form})

    def post(self, request, pk):
        my_plant = MyPlant.objects.get(pk=pk)
        form = AddMyPlantForm(request.POST, instance=my_plant)
        if form.is_valid():
            form.save()
            return redirect('show_my_plant')
        return render(request, 'plantCare/form.html', {'form': form, 'my_plant': my_plant})


class AddSoilView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddSoilForm()
        return render(request, 'plantCare/form.html', {'form': form})

    def post(self, request):
        form = AddSoilForm(request.POST)
        if form.is_valid():
            soil = form.save()
            return redirect('add_soil')
        return render(request, 'plantCare/form.html', {'form': form})


class ShowSoilView(View):
    def get(self, request):
        soil = Soil.objects.all()
        return render(request, 'plantCare/soil.html', {'soil': soil})


class DeleteSoilView(LoginRequiredMixin, View):

    def get(self, request, pk):
        soil = Soil.objects.get(pk=pk)
        return render(request, 'plantCare/soil_delete.html', {'soil': soil})

    def post(self, request, pk):
        soil = Soil.objects.get(pk=pk)
        action = request.POST.get('action')
        if action == 'tak':
            soil.delete()
            return redirect('show_soil')
        elif action == 'nie':
            return redirect('show_soil')
        return render(request, 'plantCare/soil_delete.html', {'soil': soil})


class AddReplantingView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddReplantingForm()
        return render(request, 'plantCare/form.html', {'form': form})

    def post(self, request):
        form = AddReplantingForm(request.POST)
        if form.is_valid():
            replanting = form.save()
            return redirect('add_replanting')
        return render(request, 'plantCare/form.html', {'form': form})


class ShowReplantingView(View):
    def get(self, request):
        replanting = Replanting.objects.all()
        return render(request, 'plantCare/replanting.html', {'replanting': replanting})


class AddWateringView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddWateringForm()
        instructions = """
        <div class="instructions">
        <p>INSTRUKCJA DO PODLEWANIA:</p>
        <ol>
        <li>każdą roślinę wyjmij z osłonki i powoli, równomiernie wlewaj wodę starając się 
        zmoczyć całą powierzchnię podłoża</li>
        <li>odstaw roślinę by nadmiar wody mógł odcieknąć przez otwory w doniczce</li>
        <li>wstaw roślinę do osłonki i postaw na miejscu</li>
        </ol>
        </div>"""
        return render(request, 'plantCare/form.html', {'form': form, 'instructions': instructions})

    def post(self, request):
        form = AddWateringForm(request.POST)
        if form.is_valid():
            watering = form.save()
            watering.user = request.user
            watering.save()
            return redirect('add_watering')
        return render(request, 'plantCare/form.html', {'form': form})

class ShowWateringView(View):
    def get(self, request):
        watering = Watering.objects.all()
        return render(request, 'plantCare/watering.html', {'watering': watering})


class AddFertilizationView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddFertilizationForm()
        return render(request, 'plantCare/form.html', {'form': form})

    def post(self, request):
        form = AddFertilizationForm(request.POST)
        if form.is_valid():
            fertilization = form.save()
            fertilization.user = request.user
            fertilization.save()
            return redirect('add_fertilization')
        return render(request, 'plantCare/form.html', {'form': form})

class ShowFertilizationView(View):
    def get(self, request):
        fertilization = Fertilization.objects.all()
        return render(request, 'plantCare/fertilization.html', {'fertilization': fertilization})