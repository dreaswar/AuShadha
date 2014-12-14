from django.contrib import admin

from .models import Guardian


class GuardianAdmin(admin.ModelAdmin):
    pass


admin.site.register(Guardian, GuardianAdmin)
