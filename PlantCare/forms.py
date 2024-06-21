from django import forms
from PlantCare.models import PlantType, Soil, Replanting, MyPlant, Watering, Fertilization


class AddMyPlantForm(forms.ModelForm):
    class Meta:
        model = MyPlant
        fields = ['name', 'species', 'light_requirements', 'soil_humidity', 'description']


class AddSoilForm(forms.ModelForm):
    class Meta:
        model = Soil
        fields = ['soil_type', 'soil_manufacturer', 'comment']


class AddReplantingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plant'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return f"{obj.name}"

    class Meta:
        model = Replanting
        fields = ['plant', 'old_soil_type', 'new_soil_type', 'date', 'comment']


class AddWateringForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plant'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return f"{obj.name}"
    class Meta:
        model = Watering
        fields = ['plant', 'water_content', 'date', 'water_amount', 'user']


class AddFertilizationForm(forms.ModelForm):
    class Meta:
        model = Fertilization
        fields = ['name', 'plant', 'date', 'amount']


class SearchForm(forms.Form):
    search_query = forms.CharField(required=False, max_length=20,
                                   widget=forms.TextInput(attrs={'placeholder': 'Wpisz szukaną frazę'}),
                                   label='szukana fraza')





