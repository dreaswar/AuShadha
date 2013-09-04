from django.contrib import admin
from admission.models import *
from patient.models import *
from phyexam.models import *


class AdmissionAdmin(admin.ModelAdmin):
    pass


class AdmissionComplaintAdmin(admin.ModelAdmin):
    pass


class AdmissionHPIAdmin(admin.ModelAdmin):
    pass


class AdmissionPastHistoryAdmin(admin.ModelAdmin):
    pass


class AdmissionImagingAdmin(admin.ModelAdmin):
    pass


class AdmissionInvAdmin(admin.ModelAdmin):
    pass


admin.site.register(Admission						, AdmissionAdmin)
admin.site.register(AdmissionComplaint	, AdmissionComplaintAdmin)
admin.site.register(AdmissionHPI				, AdmissionHPIAdmin)
admin.site.register(AdmissionPastHistory, AdmissionPastHistoryAdmin	)
admin.site.register(AdmissionInv				, AdmissionInvAdmin					)
admin.site.register(AdmissionImaging		, AdmissionImagingAdmin			)
