#################################################################################
# Project     : AuShadha
# Description : Models for Clinic, Departments and Staff
# Author      : Weldan Jamili, Dr.Easwar T.R (see credits)
# License     : GNU-GPL Version 3 , see docs/LICENSE.txt
# Date        : 30-09-2013
################################################################################

"""
 
 Models to handle the Clinic, Address, Staff and Departments
 User permissions, roles are set here. 
 Basic data about the Clinic is set here.
 
"""

# Import Django modules
from django.db import models

# AuShadha Imports
from AuShadha.apps.aushadha_users.models import AuShadhaUser
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm


CLINIC_NATURE_CHOICES = (
    ("primary_health_centre", "Primary Health Centre"),
    ('community_health_centre', "Community Health Centre"),
    ("poly_clinic", "Poly Clinic"),
    ("speciality_clinic", "Speciality Clinic"),
    ('district_hospital', "District Hospital"),
    ('tertiary_referral_centre', "Tertiary Referral Centre")
)

CLINIC_STAFF_ROLE = (
    ("non_clinical_staff", "Non Clinical Staff"),
    ('secretary', 'Secretary'),
    ('clinic_admin', "Clinic Administrator"),
    ('clinical_staff', "Clinical Staff"),
    ('nurse', "Nurse"),
    ('physio', "Physiotherapist"),
    ("doctor", "Doctor"),
)


class Clinic(AuShadhaBaseModel):

  """

   Model class for Clinic

   Defines the clinic

    -- name of clinic        --> Name

    -- nature_of_clinic      --> Whether its primary center / referral centre

    -- _can_add_list_or_json --> A Zope like way to set what can be contained inside this. 
                                 Objects explicitly named here will be used while setting
                                 CRUD Urls through the generate_urls() method of super.
                                 | #FIXME: A better method  / atleast name can be evolved to
                                 |        indicate this. :)

    -- _extra_url_actions    --> Other actions that are specific to this model and that can be used
                                 to generate_urls(). 

  """
  
  def __init__(self, *args, **kwargs):

      super(Clinic,self).__init__(*args, **kwargs)
      self.__model_label__ = 'clinic'
      self._parent_model = 'clinic'

      self._can_add_list_or_json = [
                          'patient',
                          'phone',
                          'address',
                          'website',
                          'email',
                          'fax',
                          'department'
                      ]
      self._extra_url_actions = ['transfer_patient','transfer_clinic','refer']


  name_of_clinic = models.CharField(max_length=200)
  nature_of_clinic = models.CharField(max_length=200, choices = CLINIC_NATURE_CHOICES)

  def __unicode__(self):
      return '%s (%s)' %(self.name_of_clinic, self.nature_of_clinic)


class Address(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):

      super(Address,self).__init__(*args, **kwargs)
      self.__model_label__ = 'address'
      self._parent_model = 'clinic'
      self._can_add_list_or_json = []
      self._extra_url_actions = []


    building_no = models.CharField(max_length=200, default= 'Tamil Nadu')    
    street_name = models.TextField()
    city_or_town = models.CharField(max_length=200, default= 'Coimbatore')
    district = models.CharField(max_length=200, default= 'Coimbatore')
    state = models.CharField(max_length=200, default= 'Tamil Nadu')
    country = models.CharField(max_length=200, default = 'India')
    postal_code = models.CharField("Postal Code", max_length=200)
    clinic = models.ForeignKey(Clinic)

    def __unicode__(self):
        return '%s - %s, %s\n %s,%s, %s -%s' %(self.building_no,
                                            self.street_name,
                                            self.city_or_town,
                                            self.district,
                                            self.state,
                                            self.country,
                                            self.postal_code
                                            )



class Phone(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):

      super(Phone,self).__init__(*args, **kwargs)
      self.__model_label__ = 'phone'
      self._parent_model = 'clinic'
      self._can_add_list_or_json = ['phone']


    country_code    = models.PositiveIntegerField(max_length = 6, default = 91)
    area_code    = models.PositiveIntegerField(max_length = 10, default = 422)
    phone_number = models.PositiveIntegerField(max_length=200)
    clinic = models.ForeignKey(Clinic)


    def __unicode__(self):
        return '%s-%s-%s' % (self.country_code, self.area_code,self.phone_number)


class Fax(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):
      super(Fax,self).__init__(*args, **kwargs)
      self.__model_label__ = 'fax'
      self._parent_model = 'clinic'


    fax_number = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic)


    def __unicode__(self):
        return '%s' % self.fax_number

class Email(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):

      super(Email,self).__init__(*args, **kwargs)
      self.__model_label__ = 'email'
      self._parent_model = 'clinic'


    email_address = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic)

    def __unicode__(self):
        return '%s' % self.email_address


class Website(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):

      super(Website,self).__init__(*args, **kwargs)
      self.__model_label__ = 'website'
      self._parent_model = 'clinic'


    website_address = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic)
    
    def __unicode__(self):
        return '%s' % self.website_address


class Department(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """

    def __init__(self, *args, **kwargs):
      super(Department,self).__init__(*args, **kwargs)
      self.__model_label__ = 'department'
      self._parent_model = 'clinic'
      self._can_add_list_or_json = ['staff']
      self._extra_url_actions = ['assign_hod','transfer_department']


    name_of_department = models.CharField(max_length=100, unique=True)
    clinic = models.ForeignKey(Clinic)

    def __unicode__(self):
        return "%s" % self.name_of_department


class Staff(AuShadhaBaseModel):

    """
     Basic Contact attributes of the Clinic
    """
  
    def __init__(self, *args, **kwargs):
      super(Staff,self).__init__(*args, **kwargs)
      self.__model_label__ = 'staff'
      self._parent_model = 'department'
      self._can_add_list_or_json = []
      self._extra_url_actions = []


    staff_detail  = models.ForeignKey(AuShadhaUser)
    clinic_staff_role = models.CharField("Staff Role",max_length=100,
                                         help_text=" This is the Role of the Staff in the Clinic",
                                         choices=CLINIC_STAFF_ROLE)
    is_staff_hod = models.BooleanField("Is Staff Head of the Department",default=None)
    department    = models.ForeignKey(Department)

    def __unicode__(self):
        return "%s" % self.staff_detail.username

    def is_staff_provider(self):
        staff_obj = self
        staff_role = self.clinic_staff_role
        if staff_role == 'doctor':
            return True
        else:
            return False
