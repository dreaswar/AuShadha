# -*- coding: utf-8 -*-
###############################################################
# PROJECT: AuShadha ICD10 Procedure Code Models
# Author : Dr. Easwar T R
# Date   : 28-08-2012
# Licence: GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################

from registry.icd10pcs.models import (
    AppCfg, 
    AppTxt, 
    CodePageRow, 
    Section, 
    BodySystem, 
    Operation, 
    BodyPart, 
    Approach, 
    Device, 
    Qualifier, 
)

from django.contrib import admin


class AppCfgAdmin(admin.ModelAdmin):
    pass

class AppTxtAdmin(admin.ModelAdmin):
    pass


class CodePageRowAdmin(admin.ModelAdmin):
    pass


class SectionAdmin(admin.ModelAdmin):
    pass

class BodySystemAdmin(admin.ModelAdmin):
    pass
    
class OperationAdmin(admin.ModelAdmin):
    pass

class BodyPartAdmin(admin.ModelAdmin):
    pass
    
class ApproachAdmin(admin.ModelAdmin):
    pass
    
class DeviceAdmin(admin.ModelAdmin):
    pass
    
class QualifierAdmin(admin.ModelAdmin):
    pass
    
    
admin.site.register(AppCfg, AppCfgAdmin)
admin.site.register(AppTxt, AppTxtAdmin)

admin.site.register(CodePageRow, CodePageRowAdmin)

admin.site.register(Section, SectionAdmin)
admin.site.register(BodySystem, BodySystemAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(BodyPart, BodyPartAdmin)
admin.site.register(Approach, ApproachAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Qualifier, QualifierAdmin)

