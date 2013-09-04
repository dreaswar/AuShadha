from icd10_pcs.models import *
import datetime
from django.contrib import admin


class PcsTableAdmin(admin.ModelAdmin):
    pass


class PcsRowAdmin(admin.ModelAdmin):
    pass


class BodyPartAdmin(admin.ModelAdmin):
    pass


class ApproachAdmin(admin.ModelAdmin):
    pass


class DeviceAdmin(admin.ModelAdmin):
    pass


class QualifierAdmin(admin.ModelAdmin):
    pass


admin.site.register(PcsTable, PcsTableAdmin)
admin.site.register(PcsRow, PcsRowAdmin)
admin.site.register(BodyPart, BodyPartAdmin)
admin.site.register(Approach, ApproachAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Qualifier, QualifierAdmin)
