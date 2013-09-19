from django.contrib import admin
from medical_history.models import MedicalHistory


class MedicalHistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(MedicalHistory, MedicalHistoryAdmin)
