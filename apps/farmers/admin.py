from django.contrib import admin
from .models import Farmer, Farm, Harvest, Crop

admin.site.register(Farmer)
admin.site.register(Farm)
admin.site.register(Harvest)
admin.site.register(Crop)
