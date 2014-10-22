from django.contrib import admin
from history.family_history.models import FamilyHistory


class FamilyHistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(FamilyHistory, FamilyHistoryAdmin)
