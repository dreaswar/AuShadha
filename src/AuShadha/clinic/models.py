from django.db import models

from django.contrib.auth.models import User
from aushadha_users.models import AuShadhaUser


"""
Model/s for Clinic module
"""

CLINIC_STAFF_ROLE = (
    ("doctor", "Doctor"),
    ('nurse', "Nurse"),
    ('physio', "Physiotherapist"),
    ("non_clinical_staff", "Non Clinical Staff"),
    ('clinical_staff', "Clinical Staff"),
    ('secretary', 'Secretary'),
    ('clinic_admin', "Clinic Administrator"),
)


# clinic model
class Clinic(models.Model):
  
    __model_label__ = 'clinic'
    _parent_model = 'clinic'

    name_of_clinic = models.CharField(max_length=200)
    address = models.TextField()
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    nature_of_clinic = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.name_of_clinic

    def get_edit_url(self):
        return 'clinic/edit/%s/' % (self.id)

    def get_del_url(self):
        return 'clinic/del/%s/' % (self.id)

    def add_patient_url(self):
        return 'clinic/%s/pat/add/%s/' % (self.name_of_clinic, self.id)

    def add_staff_url(self):
        return 'clinic/%s/staff/add/%s/' % (self.name_of_clinic, self.id)

    def add_department_url(self):
        return 'clinic/%s/department/add/%s/' % (self.name_of_clinic, self.id)

    def add_phone_url(self):
        return 'clinic/%s/phone/add/%s/' % (self.name_of_clinic, self.id)

    def add_website_url(self):
        return 'clinic/%s/website/add/%s/' % (self.name_of_clinic, self.id)

    def add_fax_url(self):
        return 'clinic/%s/fax/add/%s/' % (self.name_of_clinic, self.id)

    def add_fax_url(self):
        return 'clinic/%s/fax/add/%s/' % (self.name_of_clinic, self.id)

    def add_email_url(self):
        return 'clinic/%s/email/add/%s/' % (self.name_of_clinic, self.id)

    def add_website_url(self):
        return 'clinic/%s/website/add/%s/' % (self.name_of_clinic, self.id)

    def get_patient_list_url(self):
        return 'clinic/%s/pat/list/%s/' % (self.name_of_clinic, self.id)

    def get_staff_list_url(self):
        return 'clinic/%s/staff/list/%s/' % (self.name_of_clinic, self.id)

    def get_department_list_url(self):
        return 'clinic/%s/department/list/%s/' % (self.name_of_clinic, self.id)

    def get_phone_list_url(self):
        return 'clinic/%s/phone/list/%s/' % (self.name_of_clinic, self.id)

    def get_fax_list_url(self):
        return 'clinic/%s/fax/list/%s/' % (self.name_of_clinic, self.id)

    def get_website_list_url(self):
        return 'clinic/%s/website/list/%s/' % (self.name_of_clinic, self.id)


# Model for Departments in the Clinic
class Department(models.Model):
    name_of_department = models.CharField(max_length=100, unique=True)
    head_of_department = models.BooleanField(default=False)
    staff_name = models.ForeignKey(
        'Staff', related_name="Staff Name")
    clinic = models.ForeignKey(Clinic)

    def __unicode__(self):
        return "%s" % self.name_of_department

    class Meta:
        unique_together = (('head_of_department', "staff_name"),
                          ('head_of_department', "name_of_department"),
                          ('name_of_department', "staff_name")
                           )

    def get_edit_url(self):
        return 'clinic/department/edit/%s/' % (self.id)

    def get_del_url(self):
        return 'clinic/department/del/%s/' % (self.id)

    def get_staff_in_department_url(self):
        return 'clinic/department/staff/list/%s/' % (self.id)

    def get_hod_in_department_url(self):
        return 'clinic/department/hod/%s/' % (self.id)


# phone model
class Phone(models.Model):
    clinic = models.ForeignKey(Clinic)
    phone_number = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.phone_number

    def get_edit_url(self):
        return 'clinic/phone/edit/%s/' % (self.id)

    def get_del_url(self):
        return 'clinic/phone/del/%s/' % (self.id)


# fax model
class Fax(models.Model):
    clinic = models.ForeignKey(Clinic)
    fax_number = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.fax_number

    def get_edit_url(self):
        return 'clinic/fax/edit/%s/' % (self.id)

    def get_del_url(self):
        return 'clinic/fax/del/%s/' % (self.id)


# email model
class Email(models.Model):
    clinic = models.ForeignKey(Clinic)
    email_address = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.email_address

    def get_edit_url(self):
        return 'clinic/email/edit/%s/' % (self.id)

    def get_del_url(self):
        return 'clinic/email/del/%s/' % (self.id)


# website model
class Website(models.Model):
    clinic = models.ForeignKey(Clinic)
    website_address = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.website_address

    def get_edit_url(self):
        return 'clinic/website/edit/%s/' % (self.id)

    def get_del_url(self):
        return 'clinic/website/del/%s/' % (self.id)


# staff model
class Staff(models.Model):
    clinic = models.ForeignKey(Clinic)
#   clinic_staff_list     = models.ForeignKey(User)
    clinic_staff_list = models.ForeignKey(AuShadhaUser)
    clinic_staff_role = models.CharField("Staff Role",
                                         max_length=100,
                                         help_text=" This is the Role of the Staff in the Clinic",
                                         choices=CLINIC_STAFF_ROLE
                                         )
    #department            = models.ForeignKey(Department)
    is_staff_hod = models.BooleanField(
        "Is Staff Head of the Department",
        editable=False
    )

    class Meta:
        unique_together = (('clinic', 'clinic_staff_list'),
                           )

    def __unicode__(self):
        return "%s" % self.clinic_staff_list.username

    def save(self, *args, **kw):
        self.is_staff_hod
        super(Staff, self).save(*args, **kw)

    def _is_staff_hod(self):
        staff_obj = self
        clinic_staff = self.clinic_staff_list
        hod = Department.objects.filter(
            staff_name=clinic_staff).filter(head_of_department=True)
        if hod:
            staff_obj.is_staff_hod = True
        else:
            staff_obj.is_staff_hod = False
#        self.save()

    def is_staff_provider(self):
        staff_obj = self
        staff_role = self.clinic_staff_role
        if staff_role == 'doctor':
            return True
        else:
            return False

    def get_edit_url(self):
        return 'clinic/staff/edit/%s/' % (self.id)

    def get_del_url(self):
        return 'clinic/staff/del/%s/' % (self.id)
