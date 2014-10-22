from django.contrib import admin

from admission.admission.models import AdmissionDetail, AdmissionComplaint, \
                                       AdmissionHPI, AdmissionInv, AdmissionImaging,\
                                       AdmissionPastHistory, AdmissionROS


class AdmissionDetailAdmin(admin.ModelAdmin):
    pass


class AdmissionComplaintAdmin(admin.ModelAdmin):
    pass


class AdmissionHPIAdmin(admin.ModelAdmin):
    pass

class AdmissionPastHistoryAdmin(admin.ModelAdmin):
    pass

class AdmissionROSAdmin(admin.ModelAdmin):
    pass


class AdmissionImagingAdmin(admin.ModelAdmin):
    pass


class AdmissionInvAdmin(admin.ModelAdmin):
    pass


admin.site.register(AdmissionDetail , AdmissionDetailAdmin)
admin.site.register(AdmissionComplaint, AdmissionComplaintAdmin)
admin.site.register(AdmissionHPI, AdmissionHPIAdmin)
admin.site.register(AdmissionROS, AdmissionROSAdmin)
admin.site.register(AdmissionPastHistory, AdmissionPastHistoryAdmin)
admin.site.register(AdmissionInv, AdmissionInvAdmin	)
admin.site.register(AdmissionImaging, AdmissionImagingAdmin)
