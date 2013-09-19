from django.contrib import admin
from medication_list.models import MedicationList


class MedicationListAdmin(admin.ModelAdmin):
    pass

admin.site.register(MedicationList, MedicationListAdmin)
