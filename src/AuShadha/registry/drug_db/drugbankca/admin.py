from django.contrib import admin
from registry.drug_db.drugbankca.models import DrugBankCaDrugs


class DrugBankCaDrugsAdmin(admin.ModelAdmin):
    list_display = ['drug_name', 'drug_id']


admin.site.register(DrugBankCaDrugs, DrugBankCaDrugsAdmin)
