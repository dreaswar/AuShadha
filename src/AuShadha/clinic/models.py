from django.db import models

from django.contrib.auth.models import User
from aushadha_users.models import AuShadhaUser



"""
Model/s for Clinic module
"""

CLINIC_STAFF_ROLE = (
                      ("doctor"             , "Doctor"               ),
                      ('nurse'              , "Nurse"                ),
                      ('physio'             , "Physiotherapist"      ),
                      ("non_clinical_staff" , "Non Clinical Staff"   ),
                      ('clinical_staff'     , "Clinical Staff"       ),
                      ('secretary'          , 'Secretary'            ),
                      ('clinic_admin'       , "Clinic Administrator" ),
                     )


# clinic model
class Clinic(models.Model):
    name_of_clinic   = models.CharField(max_length=200)
    address          = models.TextField()
    state            = models.CharField(max_length=200)
    zipcode          = models.CharField(max_length=200)
    country          = models.CharField(max_length=200)
    nature_of_clinic = models.CharField(max_length=200)
    
    def __str__(self):
        return '%s' % self.name_of_clinic



# Model for Departments in the Clinic
class Department(models.Model):
    name_of_department = models.CharField(max_length = 100, unique = True)
    head_of_department = models.BooleanField(default = False)
    staff_name         = models.ForeignKey('Staff', related_name = "Staff Name")
    clinic             = models.ForeignKey(Clinic)
    
    def __unicode__(self):
         return "%s" %self.name_of_department

    class Meta:
          unique_together = ( ('head_of_department', "staff_name"), 
                              ('head_of_department', "name_of_department"), 
                              ('name_of_department', "staff_name")
                            )


# phone model
class Phone(models.Model):
    clinic       = models.ForeignKey(Clinic)
    phone_number = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.phone_number    


# fax model
class Fax(models.Model):
    clinic     = models.ForeignKey(Clinic)
    fax_number = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.fax_number  
    
# email model
class Email(models.Model):
    clinic        = models.ForeignKey(Clinic)
    email_address = models.CharField(max_length=200)  

    def __str__(self):
        return '%s' % self.email_address      
    
# website model
class Website(models.Model):
    clinic          = models.ForeignKey(Clinic)
    website_address = models.CharField(max_length=200)     

    def __str__(self):
        return '%s' % self.website_address  



# staff model
class Staff(models.Model):
    clinic                = models.ForeignKey(Clinic)
#   clinic_staff_list     = models.ForeignKey(User)     
    clinic_staff_list     = models.ForeignKey(AuShadhaUser)
    clinic_staff_role     = models.CharField("Staff Role", 
                                              max_length = 100,
                                              help_text = " This is the Role of the Staff in the Clinic",
                                              choices   = CLINIC_STAFF_ROLE
                                           )
    department            = models.ForeignKey(Department)
    is_staff_hod          = models.BooleanField("Is Staff Head of the Department", 
                                                editable = False
                                               )
    

    def _is_staff_hod(self):
        staff_obj    = self
        clinic_staff = self.clinic_staff_list
        hod = Department.objects.filter(staff_name = clinic_staff).filter(head_of_department = True)
        if hod:
            staff_obj.is_staff_hod = True
        else:
            staff_obj.is_staff_hod = False
#        self.save()


    def __unicode__(self):
        return "%s" %self.clinic_staff_list.user_name


    def save(self, *args, **kw):
        self.is_staff_hod()
        super(Staff, self).save(*args, **kw)

    class Meta:
         unique_together = (('clinic', 'clinic_staff_list'),
                            ('clinic_staff_list', 'department')
                           )
