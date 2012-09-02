from django.db import models
from django.contrib.auth.models import User

"""
Model/s for Clinic module
"""

# clinic model
class Clinic(models.Model):
    name_of_clinic = models.CharField(max_length=200)
    address = models.TextField()
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    nature_of_clinic = models.CharField(max_length=200)
    
    def __str__(self):
        return '%s' % self.name_of_clinic

# phone model
class Phone(models.Model):
    clinic = models.ForeignKey(Clinic)
    phone_number = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.phone_number    

# fax model
class Fax(models.Model):
    clinic = models.ForeignKey(Clinic)
    fax_number = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.fax_number  
    
# email model
class Email(models.Model):
    clinic = models.ForeignKey(Clinic)
    email_address = models.CharField(max_length=200)  

    def __str__(self):
        return '%s' % self.email_address      
    
# website model
class Website(models.Model):
    clinic = models.ForeignKey(Clinic)
    website_address = models.CharField(max_length=200)     

    def __str__(self):
        return '%s' % self.website_address  

# staff model
class Staff(models.Model):
    clinic = models.ForeignKey(Clinic)
    clinic_staff_list = models.ForeignKey(User)     
    
    def __str__(self):
        return '%s' % self.clinic_staff_list    
