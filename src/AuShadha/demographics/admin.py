from django.contrib import admin

from demographics.models import Guardian,Contact, Phone, EmailAndFax, Demographics


class GuardianAdmin(admin.ModelAdmin):
    pass


class ContactAdmin(admin.ModelAdmin):
    list_display = ['patient_detail', 'address',
                    'city', 'state', 'country', 'pincode']


class PhoneAdmin(admin.ModelAdmin):
    list_display = ['patient_detail', 'ISD_Code', 'STD_Code', 'phone']


class EmailAndFaxAdmin(admin.ModelAdmin):
    list_display = ['patient_detail', 'email', 'web', 'fax']
    search_fields = ['patient_detail', 'email', 'web', 'fax']


class DemographicsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Guardian, GuardianAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(EmailAndFax, EmailAndFaxAdmin)
admin.site.register(Demographics, DemographicsAdmin)
