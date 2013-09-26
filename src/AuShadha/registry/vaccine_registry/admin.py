from django.contrib import admin
from registry.vaccine_registry.models import VaccineRegistry


class VaccineRegistryAdmin(admin.ModelAdmin):
  pass

admin.site.register(VaccineRegistry, VaccineRegistryAdmin)

