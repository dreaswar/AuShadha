from django.contrib import admin
from surgical_history.models import SurgicalHistory


class SurgicalHistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(SurgicalHistory, SurgicalHistoryAdmin)
