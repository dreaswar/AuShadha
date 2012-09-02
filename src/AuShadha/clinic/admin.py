from django.contrib import admin
from clinic.models import Clinic,Phone,Fax,Email,Website,Staff

"""
Admin site for Clinic module
"""

"""
to show add clinic phone numbers form
from add clinic form 
"""
class PhoneInline(admin.StackedInline):
    model = Phone

"""
to show add clinic fax numbers form
from add clinic form 
"""
class FaxInline(admin.StackedInline):
    model = Fax
    
"""
to show add clinic email addresses form
from add clinic form 
"""
class EmailInline(admin.StackedInline):
    model = Email    
    
"""
to show add clinic website address form
from add clinic form 
"""
class WebsiteInline(admin.StackedInline):
    model = Website       
    
"""
to show add clinic staff form
from add clinic form 
"""
class StaffInline(admin.StackedInline):
    model = Staff       

"""
clinic module
"""
class ClinicAdmin(admin.ModelAdmin):
    inlines = [ PhoneInline, FaxInline, EmailInline, WebsiteInline, StaffInline, ]
    extra = 0
    
"""
phone module for clinic
will remove this if not needed 
(since we can manage this from clinic form)
"""
class PhoneAdmin(admin.ModelAdmin):
    pass
    
"""
fax module for clinic
will remove this if not needed 
(since we can manage this from clinic form)
"""
class FaxAdmin(admin.ModelAdmin):
    pass  
    
"""
email module for clinic
will remove this if not needed 
(since we can manage this from clinic form)
"""
class EmailAdmin(admin.ModelAdmin):
    pass   
    
"""
website module for clinic
will remove this if not needed 
(since we can manage this from clinic form)
"""
class WebsiteAdmin(admin.ModelAdmin):
    pass       

admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Fax, FaxAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(Website, WebsiteAdmin)
