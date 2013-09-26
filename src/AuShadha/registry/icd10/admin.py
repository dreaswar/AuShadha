from registry.icd10.models import *
import datetime
from django.contrib import admin


class ChapterAdmin(admin.ModelAdmin):
    pass


class SectionAdmin(admin.ModelAdmin):
    pass


class DiagnosisAdmin(admin.ModelAdmin):
    pass


admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
