from django.contrib import admin
from immunisation.models import Immunisation


class ImmunisationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Immunisation, ImmunisationAdmin)
