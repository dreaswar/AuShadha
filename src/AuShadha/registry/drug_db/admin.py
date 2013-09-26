from registry.drug_db.models import *
import datetime
from django.contrib import admin


class FDADrugsAdmin(admin.ModelAdmin):
    list_display = ['drug_name', 'active_ingredient', 'dosage', 'form']


admin.site.register(FDADrugs, FDADrugsAdmin)
