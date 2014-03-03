#################################################################################
# Project     : AuShadha
# Description : Admin Models for Clinic
# Author      : Weldan Jamili, Dr.Easwar T.R (see credits)
# License     : GNU-GPL Version 3 , see docs/LICENSE.txt
# Date        : 30-09-2013
################################################################################

"""
  Admin site for Clinic module
"""


from django.contrib import admin

from AuShadha.apps.clinic.models import Clinic, Department, Phone, Fax, Email, Website, Staff


class DepartmentInline(admin.StackedInline):
    """
      To Show the Departments Add Form
    """
    model = Department


class PhoneInline(admin.StackedInline):
    """
      to show add clinic phone numbers form
      from add clinic form 
    """
    model = Phone

class FaxInline(admin.StackedInline):
    """
      to show add clinic fax numbers form
      from add clinic form 
    """
    model = Fax

class EmailInline(admin.StackedInline):
    """
      to show add clinic email addresses form
      from add clinic form 
    """
    model = Email


class WebsiteInline(admin.StackedInline):
    """
      to show add clinic website address form
      from add clinic form 
    """
    model = Website

class StaffInline(admin.StackedInline):
    """
      to show add clinic staff form
      from add clinic form 
    """
    model = Staff


class ClinicAdmin(admin.ModelAdmin):
    """
      clinic module
    """
    inlines = [DepartmentInline, PhoneInline, FaxInline,
               EmailInline, WebsiteInline, ]
    extra = 0


class DepartmentAdmin(admin.ModelAdmin):
    """ Department Admin. To be removed later. """
    inlines = [StaffInline]


class PhoneAdmin(admin.ModelAdmin):
    """
      phone module for clinic
      will remove this if not needed 
      (since we can manage this from AuShadha.apps.clinic form)
    """
    pass

class FaxAdmin(admin.ModelAdmin):
    """
      fax module for clinic
      will remove this if not needed 
      (since we can manage this from AuShadha.apps.clinic form)
    """
    pass

class EmailAdmin(admin.ModelAdmin):
    """
      email module for clinic
      will remove this if not needed 
      (since we can manage this from AuShadha.apps.clinic form)
    """
    pass

class WebsiteAdmin(admin.ModelAdmin):
    """
      website module for clinic
      will remove this if not needed 
      (since we can manage this from AuShadha.apps.clinic form)
    """
    pass


class StaffAdmin(admin.ModelAdmin):
    """ Staff Admin """
    pass


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Fax, FaxAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Staff, StaffAdmin)
