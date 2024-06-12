from django.contrib import admin


from PlantCare.models import PlantType, MyPlant, Soil, Replanting, Watering

# Register your models here.
admin.site.register(PlantType)
admin.site.register(MyPlant)
admin.site.register(Soil)
admin.site.register(Replanting)
admin.site.register(Watering)
