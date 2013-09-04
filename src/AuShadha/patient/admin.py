from patient.models import *
import datetime
from django.contrib import admin


class PatientDetailAdmin(admin.ModelAdmin):
    list_display = ['patient_hospital_id',
                    'first_name', 'middle_name', 'last_name']


class PatientGuardianAdmin(admin.ModelAdmin):
    list_display = ['guardian_name', 'patient_detail']


class PatientContactAdmin(admin.ModelAdmin):
    list_display = ['patient_detail', 'address',
                    'city', 'state', 'country', 'pincode']


class PatientPhoneAdmin(admin.ModelAdmin):
    list_display = ['patient_detail', 'ISD_Code', 'STD_Code', 'phone']


class PatientEmailFaxAdmin(admin.ModelAdmin):
    list_display = ['patient_detail', 'email', 'web', 'fax']
    search_fields = ['patient_detail', 'email', 'web', 'fax']


class PatientImmunisationAdmin(admin.ModelAdmin):
    pass


class VaccineRegistryAdmin(admin.ModelAdmin):
    pass


class PatientDemographicsDataAdmin(admin.ModelAdmin):
    pass


admin.site.register(PatientDetail, PatientDetailAdmin)
admin.site.register(PatientGuardian, PatientGuardianAdmin)
admin.site.register(PatientContact, PatientContactAdmin)
admin.site.register(PatientPhone, PatientPhoneAdmin)
admin.site.register(PatientEmailFax, PatientEmailFaxAdmin)
admin.site.register(PatientImmunisation, PatientImmunisationAdmin)
admin.site.register(VaccineRegistry, VaccineRegistryAdmin)
admin.site.register(PatientDemographicsData, PatientDemographicsDataAdmin)
