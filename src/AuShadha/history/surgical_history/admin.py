from django.contrib import admin
from history.surgical_history.models import SurgicalHistory


class SurgicalHistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(SurgicalHistory, SurgicalHistoryAdmin)
