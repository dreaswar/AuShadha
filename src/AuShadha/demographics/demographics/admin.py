from django.contrib import admin
from .models import Demographics



class DemographicsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Demographics, DemographicsAdmin)
