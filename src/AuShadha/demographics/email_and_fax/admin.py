from django.contrib import admin
from .models import EmailAndFax


class EmailAndFaxAdmin(admin.ModelAdmin):
    list_display = ['patient_detail', 'email', 'web', 'fax']
    search_fields = ['patient_detail', 'email', 'web', 'fax']


admin.site.register(EmailAndFax, EmailAndFaxAdmin)

