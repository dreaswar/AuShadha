from django.contrib import admin
from patient.models import PatientDetail


class PatientDetailAdmin(admin.ModelAdmin):
    list_display = ['patient_hospital_id',
                    'first_name', 'middle_name', 'last_name']


admin.site.register(PatientDetail, PatientDetailAdmin)
