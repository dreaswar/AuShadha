from django.contrib import admin
from allergy_list.models import Allergy


class AllergyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Allergy, AllergyAdmin)
