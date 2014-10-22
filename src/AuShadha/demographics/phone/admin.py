from django.contrib import admin
from .models import Phone

class PhoneAdmin(admin.ModelAdmin):
    list_display = ['patient_detail', 'ISD_Code', 'STD_Code', 'phone']

admin.site.register(Phone, PhoneAdmin)

