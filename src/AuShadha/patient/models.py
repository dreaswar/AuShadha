################################################################################
# PROJECT: AuShadha
#          Patient Models for managing patient contact, 
#          phone, email, and Guardian details
# Author : Dr. Easwar T R
# Date   : 28-08-2012
# Licence: GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

from django.db	              import models
from django.forms	          import ModelForm
from django.core.exceptions   import ValidationError
from django 		          import forms

from django.contrib.auth.models  import User
from aushadha_base_models.models import AuShadhaBaseModel


from clinic.models import Clinic


def generic_url_maker(instance,action,id, root_object = False):
  """
    Returns the URL Pattern for any AuShadha Object
    Following the naming conventions
    instance   : an instance of a Django Model
    action     : action that URL will commit : add/edit/delete/list/
    root_object: for the list option is root_object is False, instance id will be appended to URL else no id 
                 will be appended. 
                 Eg:: to list all patients, under a clinic once a queryset is done
                 the id will be that of the clinic. But for the root object clinic since there is no db_relationship
                 that fetches a list of clinics, all clinics are fetched and listed.
  """
  #FIXME:: may be better to rely on django.contrib.contenttypes.ContentType to do a similar thing rather than using _meta  
  from AuShadha.settings import APP_ROOT_URL
  if not root_object:
    url = unicode(APP_ROOT_URL) + unicode(instance._meta.app_label)+ "/" + unicode(action) +"/" + unicode(id) +"/"
  if root_object:
    url = unicode(APP_ROOT_URL) + unicode(instance._meta.app_label)+ "/" + unicode(action) +"/"
  return url



class PatientDetail(models.Model):

	'''
	Patient Detail Model that gives the models definition and the associated methods to control the Patient models.
	
	'''
	
	__model_label__ = "detail"

	patient_hospital_id = models.CharField('Hospital ID', 
                                               max_length =15,  null = True,  blank = True, unique = True)
	first_name 	    = models.CharField(max_length =30)
	middle_name 	    = models.CharField(max_length = 30,  
                                               help_text  = "Please enter Initials / Middle Name", 
                                               blank = True,  null = True)
	last_name 	    =  models.CharField(max_length = 30, blank = True, 
                                                null       = True, 
                                                help_text  = "Enter Initials / Last Name")
	full_name 	    = models.CharField(max_length = 100, 
                                               editable   = False,
                                               null       = False, 
                                               blank      = False 
                                              )
	age 		    = models.CharField(max_length =10,  blank = True, null = True )
	sex 		    = models.CharField(max_length =6,  
                                               choices=(("Male","Male"),
                                                        ("Female","Female"),
                                                        ("Others","Others") 
                                                       ),
                                               default = "Male")
	parent_clinic       = models.ForeignKey('clinic.Clinic')


## Subclass Meta:
	class Meta:
		unique_together = ('patient_hospital_id','parent_clinic')

## Define the Unicode method for Patient Detail Model::
	def __unicode__(self):
		if self.middle_name and self.last_name:
			return "%s %s %s" %(self.first_name.capitalize(), 
                                            self.middle_name.capitalize(), 
                                            self.last_name.capitalize() 
                                           )
		elif self.last_name:
			return "%s %s" %(self.first_name.capitalize(),self.last_name.capitalize())
		else:
			return "%s %s" %(self.first_name.capitalize(),self.middle_name.capitalize())


# Defines and sets the Full Name for a Model on save. 
# This stores the value under the self.full_name attribute. 
# This is mainly intented for name display and search 
	def _set_full_name(self):
		if self.middle_name and self.last_name:
			self.full_name =  unicode(self.first_name.capitalize()  + " " + 
                                      self.middle_name.capitalize() + " " + 
                                      self.last_name.capitalize()
                                      )
		elif self.last_name:
			self.full_name = unicode(self.first_name.capitalize() + " " + 
                                     self.last_name.capitalize() 
                                     )
		else:
			self.full_name = unicode(self.first_name.capitalize() + " "+ 
                                     self.middle_name.capitalize()
                                     )
		return self.full_name

# Check DOB and Age. See Which one to set. Dont set age if DOB is given. Dont allow age > 120 to be set. 
# This should be called before Form & Model save.
# If this returns false, the save should fail raising proper Exception
	def _set_age(self):
		if self.date_of_birth:
			min_allowed_dob = datetime.datetime(1900,01,01)
			max_allowed_dob = datetime.datetime.now()
			if self.date_of_birth >= min_allowed_dob and \
                           self.date_of_birth <= max_allowed_dob:
				self.age     = "%.2f" %( round( (max_allowed_dob - self.date_of_birth).days/365.0, 2) )
				return True
			else:
				raise Exception("Invalid Date: Date should be from January 01 1900 to Today's Date")
		else:
			if self.age and int(self.age[0:3])<=120:
				self.date_of_bith = None
				return True
			else:
				raise Exception("Invalid Date of Birth / Age Supplied")
				return False



## Defines all the URLS associated with a Patient Model and the actions associated::    
## General Pattern of URL methods in all models follow the convention: 
##     get_ + 'app name' + 'model name' + '_url' 

	def get_patient_home_url(self):
		'''Returns the Home of the Patient with a specific ID. 
			 This is the place where the central actions of the 
			 Patient can be managed at one place.
			 This includes Contacts/ Admissions / OP visits etc..
		'''
		return '/AuShadha/pat/home/%s/' %self.id

	def get_patient_main_window_url(self):
		'''
			Returns the Main Window URL for the Patient which allows editing of 
			Patient details, visits, admission.
		'''
		return '/AuShadha/pat/main_window/%s/' %self.id

################################################################################

	def get_patient_detail_list_url(self):
		'''
			Returns the Listing URL for the Patient which allows editing of 
			Patient Contacts, Phone, Guardian etc..
		'''
		return '/AuShadha/pat/detail/list/%s/' %self.id

	def get_patient_detail_edit_url(self):
		'''
			Returns the Editing URL for the Patient which allows editing of 
			Patient Contacts, Phone, Guardian etc..
		'''
		return self.get_edit_url()

	def get_edit_url(self):
		'''
			Returns the Editing URL for the Patient which allows editing of 
			Patient Contacts, Phone, Guardian etc..
		'''
		return '/AuShadha/pat/detail/edit/%s/' %self.id

	def get_patient_detail_del_url(self):
		'''
			Returns the Deleting URL for the Patient.
			This action will delete all details of the patient including the 
			admission, visits, phy-exam records, media etc..
		'''
		return self.get_del_url()

	def get_del_url(self):
		'''
			Returns the Deleting URL for the Patient.
			This action will delete all details of the patient including the 
			admission, visits, phy-exam records, media etc..
		'''
		return '/AuShadha/pat/detail/del/%s/' %self.id

################################################################################

	def get_patient_contact_list_url(self):
		'''
			Returns the URL for Listing contact details for a Patient
		'''
		return '/AuShadha/pat/contact/list/%s/' %self.id

	def get_patient_contact_add_url(self):
		'''
			Returns the URL for adding contact details for a Patient
		'''
		return '/AuShadha/pat/contact/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_phone_list_url(self):
		'''
			Returns the URL for listing phone details for a Patient
		'''
		return '/AuShadha/pat/phone/list/%s/' %self.id

	def get_patient_phone_add_url(self):
		'''
			Returns the URL for adding phone details for a Patient
		'''
		return '/AuShadha/pat/phone/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_guardian_list_url(self):
		'''
			Returns the URL for List guardian details for a Patient
		'''
		return '/AuShadha/pat/guardian/list/%s/' %self.id

	def get_patient_guardian_add_url(self):
		'''
			Returns the URL for adding guardian details for a Patient
		'''
		return '/AuShadha/pat/guardian/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_email_and_fax_list_url(self):
		'''
			Returns the URL for list email and fax details for a Patient
		'''
		return '/AuShadha/pat/email_and_fax/list/%s/' %self.id

	def get_patient_email_and_fax_add_url(self):
		'''
			Returns the URL for adding email and fax details for a Patient
		'''
		return '/AuShadha/pat/email_and_fax/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_demographics_data_list_url(self):
		'''
			Returns the Demographics details for a Patient
		'''
		return '/AuShadha/pat/demographics/list/%s/' %self.id

	def get_patient_demographics_data_add_url(self):
		'''
			Returns the URL for adding Demographics details for a Patient
		'''
		return '/AuShadha/pat/demographics/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_family_history_list_url(self):
		'''
			Returns the Family History details for a Patient
		'''
		return '/AuShadha/pat/family_history/list/%s/' %self.id

	def get_patient_family_history_add_url(self):
		'''
			Returns the URL for adding family History details for a Patient
		'''
		return '/AuShadha/pat/family_history/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_social_history_list_url(self):
		'''
			Returns the Social History details for a Patient
		'''
		return '/AuShadha/pat/social_history/list/%s/' %self.id

	def get_patient_social_history_add_url(self):
		'''
			Returns the URL for adding Social History details for a Patient
		'''
		return '/AuShadha/pat/social_history/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_medical_history_list_url(self):
		'''
			Returns the Medical History details for a Patient
		'''
		return '/AuShadha/pat/medical_history/list/%s/' %self.id

	def get_patient_medical_history_add_url(self):
		'''
			Returns the URL for adding Medical History details for a Patient
		'''
		return '/AuShadha/pat/medical_history/add/%s/' %self.id

################################################################################
################################################################################

	def get_patient_surgical_history_list_url(self):
		'''
			Returns the Surgical history details for a Patient
		'''
		return '/AuShadha/pat/surgical_history/list/%s/' %self.id

	def get_patient_surgical_history_add_url(self):
		'''
			Returns the URL for adding Surgical History details for a Patient
		'''
		return '/AuShadha/pat/surgical_history/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_obstetric_history_detail_list_url(self):
		'''
			Returns the Social Obstetric details for a Patient
		'''
		return '/AuShadha/pat/obstetric_history_detail/list/%s/' %self.id

	def get_patient_obstetric_history_detail_add_url(self):
		'''
			Returns the URL for adding Obstetric History details for a Patient
		'''
		return '/AuShadha/pat/obstetric_history_detail/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_medication_list_list_url(self):
		'''
			Returns the Medication details for a Patient
		'''
		return '/AuShadha/pat/medication_list/list/%s/' %self.id

	def get_patient_medication_list_add_url(self):
		'''
			Returns the URL for adding Medication List details for a Patient
		'''
		return '/AuShadha/pat/medication_list/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_immunisation_list_url(self):
		'''
			Returns the Immnunisation details for a Patient
		'''
		return '/AuShadha/pat/immunisation/list/%s/' %self.id

	def get_patient_immunisation_add_url(self):
		'''
			Returns the URL for adding Immunisation details for a Patient
		'''
		return '/AuShadha/pat/immunisation/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_allergies_add_url(self):
		'''
		Returns the URL for adding allergy for a Patient
		'''
		return '/AuShadha/pat/allergies/add/%s/' %self.id    

	def get_patient_allergies_list_url(self):
		'''
		Returns the URL for listing allergy for a Patient
		'''
		return '/AuShadha/pat/allergies/list/%s/' %self.id    

################################################################################

################################################################################

	def get_patient_admission_list_url(self):
		'''
			Returns the URL for listing admissions for a Patient
		'''
		return '/AuShadha/pat/admission/list/%s/' %self.id  

	def get_patient_admission_add_url(self):
		'''
			Returns the URL for adding admissions for a Patient
		'''
		return '/AuShadha/pat/admission/add/%s/' %self.id  

	def get_patient_visit_list_url(self):
		'''
		Returns the URL for listing visits for a Patient
		'''
		return '/AuShadha/visit/detail/list/%s/' %self.id    

	def get_patient_visit_add_url(self):
		'''
		Returns the URL for adding visit for a Patient
		'''
		return '/AuShadha/visit/detail/add/%s/' %self.id

	def get_patient_visit_tree_url(self):
		'''
			Returns the URL for listing visits for a Patient
		'''
		return '/AuShadha/render_visit_tree/?patient_id=%s/' %self.id

################################################################################


## Defines all the methods associated with the Patient Model for manipulation and queriing..

	def check_before_you_add(self):
		'''
			Checks whether the patient has already been registered 
			in the database before adding.
		'''
		all_pat = PatientDetail.objects.all()
		hosp_id = self.patient_hospital_id
		id_list = []
		if all_pat:
			for patient in all_pat:
				id_list.append(patient.patient_hospital_id)
				if hosp_id in id_list:
					#raise Exception("Patient Already Registered")
					error = "Patient is already registered" 
					return False,error
				else:
					return True
		else:
			return True



	def save(self,*args, **kwargs):
		'''
		Custom Save Method needs to be defined. 
		This should check for:
		1. Whether the patient is registered before. 
		2. Patient DOB / Age Verfication and attribute setting
		3. Setting the full_name attribute
		'''
                self.check_before_you_add()
                self._set_full_name()
#                self._set_age()
		super(PatientDetail, self).save(*args, **kwargs)



	def has_active_admission(self):
		''' Queries whether a given patient has an active admission
				returns the string representation of the number of active admissions
				#FIXME:: May be it is better to make it return a Boolean,
				         but some feature in Template forced me to do this. 
		'''
		from admission.models import Admission
		id = self.id
		try:
			pat_obj = PatientDetail.objects.get(pk= id)
		except(TypeError, ValueError, PatientDetail.DoesNotExist):
			return False
		adm_obj = Admission.objects.filter(patient_detail = pat_obj).filter(admission_closed = False)
		adm_count = unicode(len(adm_obj))
		return adm_count

	def adm_for_pat(self): 
		''' Returns the number of admissions for a patient 
            after calling has_active_admission.
			If no admission it returns the None.
			Useful for Templates manipulation.
		'''
		from admission.models import Admission
		id = self.id
		try:
			pat_obj = PatientDetail.objects.get(pk= id)
		except(TypeError, ValueError, PatientDetail.DoesNotExist):
			return False
		if self.has_active_admission() == '0':
			return None
		else:
			all_adm_obj   = Admission.objects.filter(patient_detail = pat_obj)
			return all_adm_obj


	def has_active_visit(self):

		''' Queries whether a given patient has a active visit.
				Returns Boolean.
				Returns False in case of error. 
		'''

		from visit.models import VisitDetail
		id = self.id
		try:
			pat_obj = PatientDetail.objects.get(pk = id)
		except(TypeError, ValueError, AttributeError, PatientDetail.DoesNotExist):
			return False
		visit_obj = VisitDetail.objects.filter(patient_detail = pat_obj, is_active = True)
		if visit_obj:
			return True
		else:
			return False


	def visit_for_pat(self):

		'''
			Details the visit details for each patient. 
			This is useful for display on the Patient List table in template. 
			Can just call this method and format a table with results for a quick view.
			Can use the return value of "Visit Object" to call the is_visit_active method if needed
		'''

		from visit.models import VisitDetail
		id = self.id
		try:
			pat_obj = PatientDetail.objects.get(pk = id)
		except (TypeError, ValueError, AttributeError, PatientDetail.DoesNotExist):
			return False
		visit_obj   = VisitDetail.objects.filter(patient_detail = pat_obj)
		if not visit_obj:
			return None
		else:
			return visit_obj

	def has_contact(self):
		''' Returns a Boolean whether a particular patient has a contact or not in Database.
		'''
		id = self.id
		try:
			pat_obj = PatientDetail.objects.get(pk = id)
		except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
			return False
		address = PatientContact.objects.filter(patient_detail = pat_obj)
		if address:
			return address
		else:
			return False

	def has_phone(self):
		''' Returns a Boolean whether a particular patient has a contact or not in Database.
		'''
		id = self.id
		try:
			pat_obj = PatientPhone.objects.get(pk = id)
		except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
			return False
		phone = PatientPhone.objects.filter(patient_detail = pat_obj)
		if phone:
			return phone
		else:
			return False

	def has_guardian(self):
		''' Returns a Boolean whether a particular patient has a contact or not in Database.
		'''
		id = self.id
		try:
			pat_obj = PatientGuardian.objects.get(pk = id)
		except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
			return False
		guardian = PatientGuardian.objects.filter(patient_detail = pat_obj)
		if phone:
			return guardian
		else:
			return False

		class Meta:
			verbose_name 	    = "Basic Data"
			verbose_name_plural = "Basic Data"
			ordering 	    = ('first_name', 'middle_name','last_name','age','sex','patient_hospital_id')



class PatientGuardian(models.Model):

	'''
	Class that defines the Guardian of a Particular patient    
	'''

	__model_label__ = "guardian"

	guardian_name 		 = models.CharField(max_length = 20, blank = True, 
	                                        null = True, 
	                                        help_text ="Enter Guardian Name if Patient is a minor" 
	                                        )
	relation_to_guardian = models.CharField('Relation',
	                                        max_length =20, 
	                                        blank= True, 
	                                        null	= True, 
	                                        help_text = "Enter relationship to Guardian if Patient is a Minor", 
	                                        choices =(("Father","Father"),
	                                                  ("Mother","Mother"),
	                                                  ("Local Guardian","LocalGuardian") 
                                                     )
	                                        )
	guardian_phone 		 = models.PositiveIntegerField('Phone',
                                                       max_length= 20, 
                                                       blank = True, 
                                                       null= True
                                                       )
	patient_detail 		 = models.ForeignKey(PatientDetail, null = True, blank = True)

	def __unicode__(self):
		if self.guardian_name:
			return "%s "%(self.guardian_name)
		else:
			return "No Guardian Name Provided"

	class Meta:
		verbose_name 	    = "Guardian Details"
		verbose_name_plural = "Guardian Details"
		ordering 	    = ('patient_detail','guardian_name')

	def get_edit_url(self):
		'''
			Returns the URL for editing Guardian details for a Patient
		'''
		return '/AuShadha/pat/guardian/edit/%s/' %self.id

	def get_patient_guardian_edit_url(self):
		'''
			Returns the URL for editing Guardian details for a Patient
		'''
		return self.get_edit_url()

	def get_del_url(self):
		'''
			Returns the URL for adding Guardian details for a Patient
		'''
		return '/AuShadha/pat/guardian/del/%s/' %self.id

	def get_patient_guardian_del_url(self):
		'''
			Returns the URL for adding Guardian details for a Patient
		'''
		return self.get_del_url()


class PatientContact(models.Model):

	'''Class that defines the Contact Address of a particular patient
	'''

	__model_label__ = "contact"
	
	address_type 	= models.CharField('Type',
                                       max_length = 10, 
                                       choices =( ("Home", "Home"),
                                                  ("Office","Office"), 
                                                  ("Others","Others") 
                                       ), 
                                       default = "Home")
	address 	= models.TextField(max_length = 100, 
                                   help_text = 'limit to 100 words'
                                   )
	city 		= models.CharField(max_length = 20,
                                  default = 'Coimbatore'
                                  )
	state 		= models.CharField(max_length =20, 
                                   default= "Tamil Nadu"
                                   )
	country 	= models.CharField(max_length =20, 
                                   default = "India"
                                   )
	pincode 	= models.PositiveIntegerField(max_length =8, 
                                              null = True, 
                                              blank = True
                                              )
	patient_detail 	= models.ForeignKey(PatientDetail, 
                                        null = True, 
                                        blank = True
                                        )

	def __unicode__(self):
		if self.pincode:
			return "%s, %s, %s, %s - %s"%( self.address , 
                                           self.city    ,
                                           self.state   , 
                                           self.country , 
                                           self.pincode 
                                           )
		else:
			return "%s, %s, %s, %s"%( self.address, 
                                      self.city   , 
                                      self.state  ,
                                      self.country
                                     )

	class Meta:
		verbose_name 	    = "Address"
		verbose_name_plural = "Address"
		ordering 	        = ('patient_detail','city','state')


	def get_edit_url(self):
		'''
			Returns the URL for editing phone details for a Patient
		'''
		return '/AuShadha/pat/contact/edit/%s/' %self.id

	def get_patient_contact_edit_url(self):
		'''
			Returns the URL for editing phone details for a Patient
		'''
		return self.get_edit_url()

	def get_del_url(self):
		'''
			Returns the URL for adding phone details for a Patient
		'''
		return '/AuShadha/pat/contact/del/%s/' %self.id

	def get_patient_contact_del_url(self):
		'''
			Returns the URL for adding phone details for a Patient
		'''
		return self.get_del_url()


class PatientPhone(models.Model):
	'''
		Class that defines the Phone data of a patient
	'''
	
	__model_label__ = "phone"
		
	phone_type 	= models.CharField('Type',
                                   max_length = 10, 
                                   choices =(("Home", "Home"),
                                             ("Office","Office"),
                                             ("Mobile","Mobile"),
                                             ("Fax","Fax"),
                                             ("Others","Others") 
                                    ), 
                                    default = "Home")
	ISD_Code 	= models.PositiveIntegerField('ISD',
                                              max_length = 4, 
                                              null = True, 
                                              blank = True, 
                                              default = "0091"
                                              )
	STD_Code 	= models.PositiveIntegerField('STD',
                                               max_length = 4, 
                                               null = True, 
                                               blank = True, 
                                               default = "0422"
                                               )
	phone 		= models.PositiveIntegerField(max_length = 10, 
                                              null = True, 
                                              blank = True
                                              )
	patient_detail 	= models.ForeignKey(PatientDetail, 
                                        null = True, 
                                        blank = True
                                        )

	class Meta:
		verbose_name 	    = "Phone"
		verbose_name_plural = "Phone"
		ordering 	        = ('patient_detail',
		                       'phone_type',
		                       'ISD_Code',
		                       'STD_Code'
		                       )

	def __unicode__(self):
		if self.phone:
			return "%s- %s -%s" %(self.ISD_Code, self.STD_Code, self.phone)
		else:
			return "No Phone Number Provided"


	def get_patient_phone_edit_url(self):
		'''
			Returns the URL for editing phone details for a Patient
		'''
		return '/AuShadha/pat/phone/edit/%s/' %self.id

	def get_edit_url(self):
		return self.get_patient_phone_edit_url()

	def get_patient_phone_del_url(self):
		'''
			Returns the URL for adding phone details for a Patient
		'''
		return '/AuShadha/pat/phone/del/%s/' %self.id

	def get_del_url(self):
		return self.get_patient_phone_del_url()


class PatientEmailFax(models.Model):
	''' 
		Model that manages the Email, Fax and Web contact details of a patient
	'''
	__model_label__ = "email_and_fax"
		
	date_entered 	= models.DateTimeField(auto_now_add = True)
	email 			= models.EmailField(max_length = 75, blank = True, null = True)
	fax 			= models.PositiveIntegerField(max_length = 20, null = True, blank = True)
	web 			= models.URLField(max_length = 50, null = True, blank = True)
	patient_detail  = models.ForeignKey(PatientDetail, null = True, blank = True)

	def __unicode__(self):
		return "%s- %s -%s" %(self.email, self.fax, self.web)

	class Meta:
		verbose_name 	    = "Email, Web and Fax"
		verbose_name_plural = "Email, Web and Fax"
		ordering 	    = ('date_entered','patient_detail')


	def get_edit_url(self):
		'''
			Returns the URL for editing Email details for a Patient
		'''
		return '/AuShadha/pat/email_and_fax/edit/%s/' %self.id

	def get_patient_email_and_fax_edit_url(self):
		'''
			Returns the URL for editing Email details for a Patient
		'''
		return self.get_edit_url()

	def get_del_url(self):
		'''
			Returns the URL for adding phone details for a Patient
		'''
		return '/AuShadha/pat/email_and_fax/del/%s/' %self.id

	def get_patient_phone_del_url(self):
		'''
			Returns the URL for adding phone details for a Patient
		'''
		return self.get_del_url()




class PatientDemographicsData(models.Model):
    """
      Maintains Demographic, Social and Family data for the patient
      This has been adapted from the excellent work by GNU Health project
      However this is a very rudimentary adaptation
    """

    __model_label__ = "demographics"

    date_of_birth     = models.DateField(auto_now_add = False, 
                                         null = True, 
                                         blank = True
                                         )
    socioeconomics    = models.CharField(max_length = 100, default="Middle", 
                                         choices = (("low", "Low"), 
                                                    ("middle", "Middle" ),
                                                    ("high","High")
                                                   )
                                        )
    education         = models.CharField(max_length = 100, 
                                         default = "Graduate",
                                         choices = (('pg','Post-Graduate'),
                                                    ('g','Graduate'),
                                                    ('hs','High School'),
                                                    ('lg',"Lower Grade School"),
                                                    ('i', "Iliterate")
                                                    )
                                          )
    housing_conditions = models.TextField(max_length = 250,
                                         default = "Comfortable, with good sanitary conditions"
                         )
    religion           = models.CharField(max_length = 200)    
    religion_notes     = models.CharField(max_length = 100,
                                          null=True, 
                                          blank=True
                         )
    race               = models.CharField(max_length = 200)
    languages_known    = models.TextField(max_length = 300)
    patient_detail     = models.ForeignKey(PatientDetail,
                                           null = True  ,
                                           blank = True ,
                                           unique = True
                         )


    def __unicode__(self):
        return " Demographics for - %s" %(self.patient_detail)

    def get_edit_url(self):
        '''
        Returns the URL for editing Demographics details for a Patient
        '''
        return '/AuShadha/pat/demographics/edit/%s/' %self.id

    def get_del_url(self):
        '''
        Returns the URL for adding Demographics for a Patient
        '''
        return '/AuShadha/pat/demographics/del/%s/' %self.id

    def get_formatted_obj(self):
      return None

    def get_absolute_url(self):
      return None
      
class PatientAllergies(AuShadhaBaseModel):
  """
    Inherits from the AuShadha Base Model. 
    This defines the Allergies that the patient has. 
    The patient automatically belongs to a Clinic and has some add, edit, del 
    methods defined on him. 
    
  """

  __model_label__ = "allergies"

  allergic_to       = models.CharField(max_length = 100)
  reaction_observed = models.CharField(max_length = 100, 
                                       choices = (("rash",'Rash'),
                                                  ('angioedema','Angioedema'), 
                                                  ("anaphylaxis", "Anaphylaxis")
                                       ), 
                                       default = "Rash"
                                      )
  patient_detail = models.ForeignKey(PatientDetail,null = True,blank = True)

  def __unicode__(self):
    return "%s" %(self.allergic_to)

  def get_edit_url(self):
      '''
      Returns the URL for editing Demographics details for a Patient
      '''
      return '/AuShadha/pat/allergies/edit/%s/' %self.id

  def get_del_url(self):
      '''
      Returns the URL for adding Demographics for a Patient
      '''
      return '/AuShadha/pat/allergies/del/%s/' %self.id



class PatientImmunisation(AuShadhaBaseModel):
  """
    Inherits from the AuShadha Base Model. 
    This defines the Immunisation that the patient has had. 
    The patient automatically belongs to a Clinic and has some add, edit, del 
    methods defined on him.
    
  """

  __model_label__ = "immunisation"

#  vaccine_name     = models.CharField(max_length = 100)
  vaccine_detail    = models.ForeignKey('VaccineRegistry')
  route             = models.CharField(max_length = 30,
                                       choices=(("im", "IM"), 
                                                ("deep_im", "Deep IM"),
                                                ("iv", "Intravenous"),
                                                ("sc", "Sub Cutaneous"),
                                                ("oral", "Oral")
                                        ), 
                                        default="IM" 
                      )
  injection_site    = models.CharField(max_length = 100, 
                                       choices=(("lue", "Left Upper Arm"), 
                                                ("rue", "Right Upper Arm"),
                                                ("lb",  "Left Buttock"),
                                                ("rb",  "Right Buttock"),
                                                ("abd", "Abdomen"),
                                                ("oral", "Oral")
                                        ), 
                                        default="Right Upper Arm"
                      )
  dose              = models.CharField(max_length = 100)
  administrator     = models.ForeignKey(User)
  vaccination_date  = models.DateField(auto_now_add = False)
  next_due          = models.DateField(auto_now_add= False)
  adverse_reaction  = models.TextField(max_length = 100, default = "None")
  patient_detail    = models.ForeignKey(PatientDetail,null = True,blank = True)


  def __unicode__(self):
    return "%s" %(self.vaccine_detail)

  def save(self,*args, **kwargs):
    self.__model_label__ = "immunisation"
    super(PatientImmunisation, self).save(*args, **kwargs)


  def get_edit_url(self):
      '''
      Returns the URL for editing Demographics details for a Patient
      '''
      return '/AuShadha/pat/%s/edit/%s/' %(self.__model_label__, self.id)

  def get_del_url(self):
      '''
      Returns the URL for adding Demographics for a Patient
      '''
      return '/AuShadha/pat/%s/del/%s/' % (self.__model_label__,self.id)


class VaccineRegistry(models.Model):
  """
    Registry for the Vaccines
    This contains the details of vaccine, VIS, Manufacturer, Lot #, Expiration etc..
  """
  vaccine_name        = models.CharField(max_length = 100)
  manufacturer        = models.CharField(max_length = 100)
  lot_number          = models.CharField(max_length = 100)
  manufacturing_date  = models.DateField(auto_now_add = False)
  expiry_date         = models.DateField(auto_now_add = False)
  vis                 = models.TextField("Vaccine Information Statement", 
                                         max_length = 1000, 
                                         blank = True, 
                                         null = True
                        )

  def __unicode__(self):
    return "%s" %(self.vaccine_name)

  def save(self,*args, **kwargs):
    self.__model_label__ = "vaccine_registry"
    super(VaccineRegistry, self).save(*args, **kwargs)

  def get_edit_url(self):
      '''
      Returns the URL for editing Vaccine Registry
      '''
      return '/AuShadha/vaccine_registry/%s/edit/%s/' %(self.__model_label__, self.id)

  def get_del_url(self):
      '''
      Returns the URL for adding Vaccine Registry
      '''
      return '/AuShadha/vaccine_registry/%s/del/%s/' % (self.__model_label__,self.id)



class PatientMedicationList(AuShadhaBaseModel):
  """
    Inherits from the AuShadha Base Model. 
    This defines the medication list that the patient is currently having. 
    The patient automatically belongs to a Clinic and has some add, edit, del 
    methods defined on him. 
    
  """

  __model_label__ = "medication_list"

  medication        = models.CharField(max_length = 100, 
                                       help_text = "Only Generic Names.."
                                       )
  strength          = models.CharField(max_length = 100)
  dosage            = models.CharField(max_length = 100, 
                                       help_text = "OD, BD, TDS, QID, HS, SOS, PID etc.."
                                       )
  prescription_date = models.DateField(auto_now_add = False)
  prescribed_by     = models.CharField(max_length = 100, 
                                      choices = (("internal", "Internal"),
                                                  ("external","External")
                                                ), 
                                      default = "Internal"
                                     )
  currently_active  = models.BooleanField(default = True)
  patient_detail    = models.ForeignKey(PatientDetail,null = True,blank = True)

  def __unicode__(self):
    return "%s" %(self.medication)

  def get_edit_url(self):
      '''
      Returns the URL for editing Demographics details for a Patient
      '''
      return '/AuShadha/pat/medication_list/edit/%s/' %self.id

  def get_del_url(self):
      '''
      Returns the URL for adding Demographics for a Patient
      '''
      return '/AuShadha/pat/medication_list/del/%s/' %self.id



class PatientFamilyHistory(AuShadhaBaseModel):
  """
    Inherits from the AuShadha Base Model. 
    This defines the Family Medical History that the patient has had. 
    The patient automatically belongs to a Clinic and has some add, edit, del 
    methods defined on him. 
    
  """

  __model_label__ = "family_history"

  family_member = models.CharField(max_length = 100, 
                                   help_text = "mention only relationship.."
                                   ) 
  deceased      = models.BooleanField(default = False)
  age           = models.PositiveIntegerField()
  disease       = models.CharField(max_length = 100, 
                                   help_text = "mention diagnosis as stated by patient / as per reports"
                                   )
  age_at_onset      = models.PositiveIntegerField()
  patient_detail    = models.ForeignKey(PatientDetail,
                                        null = True,
                                        blank = True
                                        )

  def __unicode__(self):
    return "%s" %(self.family_member)

  def get_edit_url(self):
      '''
      Returns the URL for editing Demographics details for a Patient
      '''
      return '/AuShadha/pat/family_history/edit/%s/' %self.id

  def get_del_url(self):
      '''
      Returns the URL for adding Demographics for a Patient
      '''
      return '/AuShadha/pat/family_history/del/%s/' %self.id


class PatientSocialHistory(AuShadhaBaseModel):
  """
    Inherits from the AuShadha Base Model. 
    This defines the Social History that the patient has had. 
    The patient automatically belongs to a Clinic and has some add, edit, del 
    methods defined on him. 
    
  """

  exercise_choices = (('sendentary', "Sedentary"), 
                       ("active lifestyle", "Active, but no Exercise"), 
                       ("minimal","Minimal"),('moderate','Moderate'), 
                       ('extreme',"Extreme")
                      )

  sexual_preference_choices = (("opposite_sex", "Opposite Sex"), 
                               ('same_sex', "Same Sex"), 
                              ("both","Both"),
                              ('neither','Neither')
                          )

  marital_status_choices = (('single', "Single"), 
                            ("married", "Married"), 
                            ("divorced","Divorced"),
                            ('separated','Separated'),
                            ('widowed','Widowed'),
                            ('living with partner','Living with Partner')
                           )

  abuse_frequency = (('none',"None"),('former',"Former"),
                     ('everyday',"Everyday"),("periodic","Periodic")
                    )

  diet_choices = (
                  ('well_balanced',"Well Balanced"),
                  ('vegetarian',"Vegetarian"),
                  ('jain',"Jain"),
                  ('vegan',"Vegan"),
                  ('non_vegetarian',"Non-Vegetarian"),
                  ("junk","Junk"),
                  ("others","Others")
                 )

  marital_status        = models.CharField(max_length = 250, 
                                           choices=marital_status_choices, 
                                           default="Single"
                                           )
  marital_status_notes  = models.CharField(max_length = 250, 
                                           null=True, 
                                           blank=True
                                           )
  occupation            = models.CharField(max_length = 100)
  occupation_notes      = models.CharField(max_length = 100, 
                                           null=True, 
                                           blank=True
                                           )
  exercise              = models.CharField(max_length = 100, 
                                           choices=exercise_choices, 
                                           default="Active but no Exercise"
                                           )
  exercise_notes        = models.CharField(max_length = 100, 
                                           null=True, 
                                           blank=True
                                           )
  diet                  = models.CharField(max_length = 100, 
                                           choices=diet_choices, 
                                           default="Well Balanced"
                                           )
  diet_notes            = models.CharField(max_length = 100, null=True, blank=True)
  home_occupants        = models.CharField(max_length = 300)
  home_occupants_notes  = models.CharField(max_length = 100, 
                                           null=True, 
                                           blank=True
                                           )  
  pets                  = models.CharField(max_length = 300, default = "None")
  pets_notes            = models.CharField(max_length = 300, 
                                           null=True, 
                                           blank=True
                                           )
  alcohol               = models.CharField(max_length = 250, 
                                           choices=abuse_frequency, 
                                           default="None"
                                           )
  alcohol_no            = models.CharField(max_length = 100, null=True, blank=True)
  alcohol_notes         = models.CharField(max_length = 250, null=True, blank=True)  
  tobacco               = models.CharField(max_length = 250, 
                                           choices=abuse_frequency, 
                                           default="None"
                                           )
  tobacco_no            = models.CharField(max_length = 250, null=True, blank=True)
  tobacco_notes         = models.CharField(max_length = 250, null=True, blank=True)
  drug_abuse            = models.CharField(max_length = 250, 
                                           choices=abuse_frequency, 
                                           default="None"
                                           )
  drug_abuse_notes      = models.CharField(max_length = 250, null=True, blank=True)
  sexual_preference     = models.CharField(max_length = 100, 
                                           choices= sexual_preference_choices, 
                                           default="Opposite Sex"
                                           )
  sexual_preference_notes = models.CharField(max_length = 100, null=True, blank=True)
  current_events          = models.TextField(max_length = 300, 
                                     help_text = "Any ongoing / coming up issues in family having a bearing on treatment",
                                     default = "None"
                                     )
  patient_detail  = models.ForeignKey(PatientDetail,null = True,blank = True, unique = True)

  def __unicode__(self):
    return "%s" %(self.patient_detail)

  def save(self, *args, **kwargs):
    self.__model_label__ = "social_history"
    super(PatientSocialHistory, self).save(*args, **kwargs)

  def get_edit_url(self):
      '''
      Returns the URL for editing Social details for a Patient
      '''
      return '/AuShadha/pat/social_history/edit/%s/' %self.id

  def get_del_url(self):
      '''
      Returns the URL for adding Social for a Patient
      '''
      return '/AuShadha/pat/social_history/del/%s/' %self.id




class PatientICD10(AuShadhaBaseModel):
  '''
    Placeholder for ICD 10 Codes
  '''

class PatientCPC(AuShadhaBaseModel):
  '''
  Placeholder for CP Codes
  '''

class PatientMedicalHistory(AuShadhaBaseModel):
  """
  Inherits from the AuShadha Base Model.
  This defines the Medical History that the patient has had.
  The patient automatically belongs to a Clinic and has some add, edit, del
  methods defined on him.
  """
  
  from obs_and_gyn.models import ObstetricHistoryDetail

  __model_label__ = "medical_history"

  disease         = models.CharField(max_length = 250)
  icd_10_code     = models.ForeignKey("PatientICD10",null=True, blank=True)
  status          = models.CharField("Status of the Disease",
                                      max_length = 250,
                                      null=True,
                                      blank=True
                    )
  active                = models.BooleanField("Active Diseaase")
  infectious_disease    = models.BooleanField()
  severity              = models.CharField(max_length = 100)
  allergic_disease      = models.BooleanField()
  pregnancy_warning     = models.ForeignKey('obs_and_gyn.ObstetricHistoryDetail',
                                            blank=True,
                                            null = True
                          )
  date_of_diagnosis     = models.DateField(auto_now_add = False,
                                           null=True,
                                           blank = True
                          )
  healed                = models.BooleanField()
  remarks               = models.TextField(max_length = 300,
                                           help_text  = "Any Other Remarks",
                                           default    = "None"
                          )
  patient_detail  = models.ForeignKey(PatientDetail,
                                      null  = True,
                                      blank = True,
                    )


  def __unicode__(self):
    return "%s" %(self.patient_detail)

  def save(self, *args, **kwargs):
    self.__model_label__ = "medical_history"
    super(PatientMedicalHistory, self).save(*args, **kwargs)

  def get_edit_url(self):
    '''
    Returns the URL for editing Medical History details for a Patient
    '''
    return '/AuShadha/pat/%s/edit/%s/' %(self.__model_label__, self.id)

  def get_del_url(self):
    '''
    Returns the URL for deleting Medical History detail for a Patient
    '''
    return '/AuShadha/pat/%s/del/%s/' %(self.__model_label__, self.id)


class PatientSurgicalHistory(AuShadhaBaseModel):
  """
  Inherits from the AuShadha Base Model.
  This defines the Surgical History that the patient has had.
  The patient automatically belongs to a Clinic and has some add, edit, del
  methods defined on him.

  """
  from obs_and_gyn.models import ObstetricHistoryDetail

  __model_label__ = "surgical_history"

  description     = models.CharField(max_length = 250)
  icd_10_code     = models.ForeignKey("PatientICD10",null=True, blank=True)
  cpc_code        = models.ForeignKey("PatientCPC",null=True, blank=True)
  base_condition  = models.CharField("Base Condition",
                                    max_length = 250,
                                    null       = True,
                                    blank      = True
                    )
  med_condition    = models.ForeignKey("PatientMedicalHistory",
                                        null  = True,
                                        blank = True
                     )
  classification   = models.CharField(max_length = 250, null=True, blank = True)
  healed           = models.BooleanField()
  date_of_surgery  = models.DateField(auto_now_add = False,
                                       null  = True,
                                       blank = True
                       )
  remarks          = models.TextField(max_length = 300,
                                      help_text  = "Any Other Remarks",
                                      default    = "None"
                     )
  patient_detail  = models.ForeignKey(PatientDetail,
                                      null  = True,
                                      blank = True,
                    )


  def __unicode__(self):
    return "%s" %(self.patient_detail)

  def save(self, *args, **kwargs):
    self.__model_label__ = "surgical_history"
    super(PatientSurgicalHistory, self).save(*args, **kwargs)

  def get_edit_url(self):
    '''
    Returns the URL for editing Surgical History details for a Patient
    '''
    return '/AuShadha/pat/%s/edit/%s/' %(self.__model_label__, self.id)

  def get_del_url(self):
    '''
    Returns the URL for deleting Surgical History detail for a Patient
    '''
    return '/AuShadha/pat/%s/del/%s/' %(self.__model_label__, self.id)

    

## Modelform definition of Patients.

class PatientSocialHistoryForm(ModelForm):
	class Meta:
		model = PatientSocialHistory
		exclude = ('patient_detail','parent_clinic')

	#home_occupants = forms.MultipleChoiceField(choices=())
	#pets 					 = forms.MultipleChoiceField(choices=())

	#def clean_home_occupants(self):
		#home_occupants = self.cleaned_data['home_occupants']
		#print "Home Occupants are", home_occupants
		#return home_occupants

  #def clean_pets(self):
    

	def __init__(self, *args, **kwargs):
		super(PatientSocialHistoryForm, self).__init__(*args, **kwargs)
		text_fields = [
                  {"field"           : 'marital_status',
		           'max_length'      :  100         ,
		           "data-dojo-type"  : "dijit.form.Select",
		           "data-dojo-props" : r"'required' :true"
		          },
                  {"field"           : 'marital_status_notes',
		           'max_length'      :  100         ,
		           "data-dojo-type"  : "dijit.form.ValidationTextBox",
		           "data-dojo-props" : r"'required' :false ,placeHolder:'Any Other Notes...'"
		          },
		          {"field"           : 'occupation',
		           'max_length'      :  100         ,
		           "data-dojo-type"  :  "dijit.form.Select",
		           "data-dojo-props" :  r"'required' : true"
		          },
                  {"field"           : 'occupation_notes',
                   'max_length'      :  100         ,
                   "data-dojo-type"  : "dijit.form.ValidationTextBox",
                   "data-dojo-props" : r"'required' :false,placeHolder:'Others '"
                  },
                  {"field"           : 'exercise',
                   'max_length'      : 100,
                   "data-dojo-type"  : "dijit.form.Select",
		           "data-dojo-props" : r"'required' : true"
                  },
                  {"field"           : 'exercise_notes',
                   'max_length'      :  100         ,
                   "data-dojo-type"  : "dijit.form.ValidationTextBox",
                   "data-dojo-props" : r"'required' :false,placeHolder:'Other Notes...'"
		          },
                  {"field"           : 'diet',
                   'max_length'      : 100,
                   "data-dojo-type"  : "dijit.form.Select",
		           "data-dojo-props" : r"'required' : true"
                  },
                  {"field"           : 'diet_notes',
		           'max_length'      :  100         ,
		           "data-dojo-type"  : "dijit.form.ValidationTextBox",
		           "data-dojo-props" : r"'required' :false,placeHolder:'Specify'"
		          },
                  {"field"           : 'home_occupants',
                   'max_length'      : 150,
                   "data-dojo-type"  : "dijit.form.MultiSelect",
		           "data-dojo-props" : r"'required' : true"
                  },
                  {"field"           : 'home_occupants_notes',
		           'max_length'      :  100         ,
		           "data-dojo-type"  : "dijit.form.ValidationTextBox",
		           "data-dojo-props" : r"'required' :false,placeHolder:'Other details ?'"
		          },
                  {"field"           : 'pets',
                   'max_length'      : 150,
                   "data-dojo-type"  : "dijit.form.MultiSelect",
		           "data-dojo-props" : r"'required' : true"
                  },
                  {"field"            : 'pets_notes',
                    'max_length'      : 100         ,
                    "data-dojo-type"  : "dijit.form.ValidationTextBox",
                    "data-dojo-props" : r"'required' :false,placeHolder:'Notes'"
		          },
                  {"field"           : 'alcohol',
                   'max_length'      : 150,
                   "data-dojo-type"  : "dijit.form.Select",
		           "data-dojo-props" : r"'required' : true"
                  },
                  {"field"            : 'alcohol_no',
                    'max_length'      :  ""         ,
                    "data-dojo-type"  : "dijit.form.Select",
                    "data-dojo-props" : r"'required' :false"
		          },
                  {"field"            : 'alcohol_notes',
		           'max_length'       :  100         ,
		           "data-dojo-type"   : "dijit.form.ValidationTextBox",
		           "data-dojo-props"  : r"'required' :false,placeHolder:'Any Other Notes...'"
		           },
                   {"field"            : 'tobacco',
                    'max_length'       : 150,
                    "data-dojo-type"   : "dijit.form.Select",
		            "data-dojo-props"  : r"'required' : true"
                   },
                   { "field"           : 'tobacco_no',
                    'max_length'       :  ""         ,
                    "data-dojo-type"   : "dijit.form.Select",
                    "data-dojo-props"  : r"'required' :false"
		           },
                   {"field"            : 'tobacco_notes',
		            'max_length'       :  200         ,
		            "data-dojo-type"   : "dijit.form.ValidationTextBox",
		            "data-dojo-props"  : r"'required' :false,placeHolder:'Any Other Notes...'"
		           },
                   { "field"           : 'drug_abuse',
                     'max_length'      : 100,
                     "data-dojo-type"  : "dijit.form.Select",
		             "data-dojo-props" : r"'required' : true"
                   },
                   {"field"           : 'drug_abuse_notes',
                    'max_length'      : 150,
                    "data-dojo-type"  : "dijit.form.ValidationTextBox",
		            "data-dojo-props" : r"'required' : false,placeHolder:'Details..'"
                   },
                   {"field"           : 'sexual_preference',
                    'max_length'      : 100,
                    "data-dojo-type"  : "dijit.form.Select",
		            "data-dojo-props" : r"'required' : true"
                   },
                   {"field"           : 'sexual_preference_notes',
                    'max_length'      : 250,
                    "data-dojo-type"  : "dijit.form.ValidationTextBox",
		            "data-dojo-props" : r"'required' : false,placeHolder:'Other details'"
                   },
                   {"field"           : 'current_events',
                    'max_length'      : 250,
                    "data-dojo-type"  : "dijit.form.Textarea",
		            "data-dojo-props" : r"'required' : false,placeHolder:'Notes about specific events in family that has bearing on treatment'"
                   }
	        ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']


class PatientImmunisationForm(ModelForm):

	class Meta:
		model = PatientImmunisation
		exclude = ('patient_detail','parent_clinic')
	def __init__(self, *args, **kwargs):
		super(PatientImmunisationForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'vaccine_detail',
		                'max_length'    :  30         ,
		                "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required': true"
		                },
		               {"field": 'route',
		                'max_length'    :  30         ,
		               "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
		               },
		               {"field": 'injection_site',
		                'max_length'    :  30         ,
		               "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
		               },
		               {"field": 'dose',
		                'max_length'    :  30         ,
		               "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
		               },
		               {"field": 'administrator',
		                'max_length'    :  30         ,
		               "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required': true"
		               },
		               {"field": 'vaccination_date',
		                'max_length'    :  30         ,
		               "data-dojo-type": "dijit.form.DateTextBox",
		                "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
		               },
		               {"field": 'next_due',
		                'max_length'    :  30         ,
		               "data-dojo-type": "dijit.form.DateTextBox",
		                "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
		               },

                   {"field": 'adverse_reaction',
                   'max_length':150,
                   "data-dojo-type": "dijit.form.Textarea",
		                "data-dojo-props": r"'required' : true ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
                   }
	        ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']

class PatientMedicationListForm(ModelForm):

	class Meta:
		model = PatientMedicationList
		exclude = ('patient_detail','parent_clinic')
	def __init__(self, *args, **kwargs):
		super(PatientMedicationListForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'medication',
		                'max_length'    :  30         ,
		                "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' :'true' ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
		                },
		               {"field": 'strength',
		                'max_length'    :  3         ,
		               "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
		               },
                   {"field": 'dosage',
                   'max_length':30,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
                   },
                   {"field": 'prescription_date',
                   'max_length':30,
                   "data-dojo-type": "dijit.form.DateTextBox",
		                "data-dojo-props": r"'required' : 'true'"
                   },
                   {"field": 'prescribed_by',
                   'max_length':30,
                   "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
                   },
                   {"field": 'currently_active',
                   'max_length':2,
                   "data-dojo-type": "dijit.form.CheckBox",
		                "data-dojo-props": r""
                   }
	        ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']

class PatientFamilyHistoryForm(ModelForm):

	class Meta:
		model = PatientFamilyHistory
		exclude = ('patient_detail','parent_clinic')
	def __init__(self, *args, **kwargs):
		super(PatientFamilyHistoryForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'family_member',
		                'max_length'    :  100         ,
		                "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' :true ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
		                },
		               {"field": 'disease',
		                'max_length'    :  150         ,
		               "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : false ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
		               },
                   {"field": 'age_at_onset',
                   'max_length':30,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : false ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
                   },
                   {"field": 'deceased',
                   'max_length':2,
                   "data-dojo-type": "dijit.form.CheckBox",
		                "data-dojo-props": r""
                   },
                   {"field": 'age',
                   'max_length':30,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : false ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
                   }
	        ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']


class PatientAllergiesForm(ModelForm):

	class Meta:
		model = PatientAllergies
		exclude = ('patient_detail','parent_clinic')
	def __init__(self, *args, **kwargs):
		super(PatientAllergiesForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'allergic_to',
		                'max_length'    :  100        ,
		                "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' :true ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
		                },
		               {"field": 'reaction_observed',
		                'max_length'    :  100         ,
		               "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' : true "
		               }
	        ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']


class PatientDetailForm(ModelForm):

	class Meta:
		model = PatientDetail
	def __init__(self, *args, **kwargs):
		super(PatientDetailForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'first_name',
		                'max_length'    :  30         ,
		                "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' :'true' ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
		                },
		               {"field": 'middle_name',
		                'max_length'    :  30         ,
		               "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
		               },
                   {"field": 'last_name',
                   'max_length':30,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
                   },
                   {"field": 'patient_hospital_id',
		                'max_length'    :  30         ,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
                   },
                   {"field": 'age',
		                'max_length'    :  30         ,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'\\d{1,3}','invalidMessage' : 'Invalid Character. Only Numbers are allowed'"
                   },
                   {"field"    : 'sex',
		                'max_length'    :  30         ,
                   "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'','invalidMessage' : ''"
                   },
                   {
                     "field"          : "parent_clinic"     , 
                     "max_length"     : 30                  , 
                     "data-dojo-type" : "dijit.form.Select" , 
                     "data-dojo-props": r"'required':'true', 'regExp': '', 'invalidMessage': 'Please select a value' "
                   }
	        ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']


class PatientGuardianForm(ModelForm):

	class Meta:
		model   = PatientGuardian
		exclude = ('patient_detail',)
	def __init__(self, *args, **kwargs):
		super(PatientGuardianForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'guardian_name',
		                'max_length'    :  30         ,
		                "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' :'true' ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
		                },
		               {"field": 'relation_to_guardian',
		                'max_length'    :  30         ,
		               "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
		               },
                   {"field": 'guardian_phone',
                   'max_length':30,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
                   }
		              ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']

class PatientContactForm(ModelForm):

	class Meta:
		model   = PatientContact
		exclude = ("patient_detail",)
	def __init__(self, *args, **kwargs):
		super(PatientContactForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'address_type',
		                'max_length'    :  30         ,
		                "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' :'true' ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
		                },
		               {"field": 'address',
		                'max_length'    :  100         ,
		                "data-dojo-type": "dijit.form.Textarea",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z0-9-:;/\#_]','invalidMessage' : 'Invalid Character'"
		               },
                   {"field": 'city',
                   'max_length':30,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z -]+','invalidMessage' : 'Invalid Character'"
                   },
                   {"field"          : 'state',
		                'max_length'     :  30         ,
                   "data-dojo-type"  : "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z -]+','invalidMessage' : 'Invalid Character'"
                   },
                   {"field"          : 'pincode',
		                'max_length'     :  7         ,
                   "data-dojo-type"  : "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
                   },
                   {"field"          : 'country',
		                'max_length'     :  30         ,
                   "data-dojo-type"  : "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : ''"
                   },
		              ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length']      = field['max_length']


class PatientPhoneForm(ModelForm):
	class Meta:
		model   = PatientPhone
		exclude = ("patient_detail",)
	def __init__(self, *args, **kwargs):
		super(PatientPhoneForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'ISD_Code',
		                'max_length'    :  5         ,
		                "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' :'true' ,'regExp':'[\\d]+','invalidMessage':'Invalid Character' "
		                },
		               {"field": 'STD_Code',
		                'max_length'    :  6         ,
		               "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
		               },
                   {"field": 'phone',
                   'max_length':15,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
                   },
                   {"field": 'phone_type',
		                'max_length'    :  30         ,
                   "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
                   }
		              ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']

class PatientEmailFaxForm(ModelForm):
	class Meta:
		model   = PatientEmailFax
		exclude = ('patient_detail',)



class PatientDemographicsDataForm(ModelForm):

	class Meta:
		model = PatientDemographicsData
		exclude = ('patient_detail',)
	def __init__(self, *args, **kwargs):
		super(PatientDemographicsDataForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'date_of_birth',
		                'max_length'    :  30         ,
		                "data-dojo-type": "dijit.form.DateTextBox",
		                "data-dojo-props": r"'required' :true ,'regExp':'','invalidMessage':'Invalid Character' "
		                },
		               {"field": 'socioeconomics',
		                'max_length'    :  30         ,
		               "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
		               },
                   {"field": 'education',
                   'max_length':30,
                   "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
                   },
                   {"field": 'housing_conditions',
		                'max_length'    :  100         ,
                   "data-dojo-type": "dijit.form.Textarea",
		                "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
                   },
                   {"field"    : 'religion',
		                'max_length'    :  30         ,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : ''"
                   },
                  {"field"         : 'religion_notes',
		                'max_length'    :  100         ,
		                "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' :false,placeHolder:'Any Other Notes...'"
		                },
                   {
                     "field"          : "race"     , 
                     "max_length"     : 30                  , 
                     "data-dojo-type" : "dijit.form.ValidationTextBox" , 
                     "data-dojo-props": r"'required':true, 'regExp': '', 'invalidMessage': 'Please select a value' "
                   },
                   {
                     "field"          : "languages_known"     , 
                     "max_length"     : 100                  , 
                     "data-dojo-type" : "dijit.form.Textarea" , 
                     "data-dojo-props": r"'required':true, 'regExp': '', 'invalidMessage': 'Please select a value' "
                   }
	        ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']


class PatientMedicalHistoryForm(ModelForm):
  class Meta:
    model = PatientMedicalHistory
    exclude = ('patient_detail','parent_clinic')

  def __init__(self, *args, **kwargs):
    super(PatientMedicalHistoryForm, self).__init__(*args, **kwargs)
    text_fields = [{"field"         : 'disease',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.ValidationTextBox",
                    "data-dojo-props": r"'required' :true"
                    },
                  {"field"         : 'icd_10_code',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.Select",
                    "data-dojo-props": r"'required' :false"
                    },
                   {"field": 'status',
                    'max_length'    :  100         ,
                   "data-dojo-type": "dijit.form.Select",
                    "data-dojo-props": r"'required' : false"
                   },
                    {"field"         : 'infectious_disease',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.CheckBox",
                    "data-dojo-props": r"'required' :false"
                    },
                   {"field": 'active',
                   'max_length':100,
                   "data-dojo-type": "dijit.form.CheckBox",
                    "data-dojo-props": r"'required' : false"
                   },
                  {"field"         : 'severity',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.ValidationTextBox",
                    "data-dojo-props": r"'required' :false,placeHolder:'Severity of disease'"
                    },
                   {"field": 'allergic_disease',
                   'max_length':100,
                   "data-dojo-type": "dijit.form.CheckBox",
                    "data-dojo-props": r"'required' : false"
                   },
                  {"field"         : 'pregnancy_warning',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.Select",
                    "data-dojo-props": r"'required' :false"
                    },
                   {"field": 'date_of_diagnosis',
                   'max_length':150,
                   "data-dojo-type": "dijit.form.DateTextBox",
                    "data-dojo-props": r"'required' : false"
                   },
                  {"field"         : 'healed',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.CheckBox",
                    "data-dojo-props": r"'required' :false"
                    },
                   {"field": 'remarks',
                   'max_length':150,
                   "data-dojo-type": "dijit.form.Textarea",
                    "data-dojo-props": r"'required' : false"
                   }
          ]
    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['max_length'] = field['max_length']


class PatientSurgicalHistoryForm(ModelForm):
  class Meta:
    model = PatientSurgicalHistory
    exclude = ('patient_detail','parent_clinic')

  def __init__(self, *args, **kwargs):
    super(PatientSurgicalHistoryForm, self).__init__(*args, **kwargs)
    text_fields = [{"field"         : 'description',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.ValidationTextBox",
                    "data-dojo-props": r"'required' :true"
                    },
                  {"field"         : 'icd_10_code',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.Select",
                    "data-dojo-props": r"'required' :false"
                    },
                   {"field": 'cpc_code',
                    'max_length'    :  100         ,
                   "data-dojo-type": "dijit.form.Select",
                    "data-dojo-props": r"'required' : false"
                   },
                    {"field"         : 'base_condition',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.ValidationTextBox",
                    "data-dojo-props": r"'required' :false"
                    },
                   {"field": 'med_condition',
                   'max_length':100,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
                    "data-dojo-props": r"'required' : false"
                   },
                  {"field"         : 'healed',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.CheckBox",
                    "data-dojo-props": r"'required' :false"
                    },
                  {"field"         : 'classification',
                    'max_length'    :  100         ,
                    "data-dojo-type": "dijit.form.ValidationTextBox",
                    "data-dojo-props": r"'required' :false,placeHolder:'Any other Classification..'"
                    },
                   {"field": 'date_of_surgery',
                   'max_length':100,
                   "data-dojo-type": "dijit.form.DateTextBox",
                    "data-dojo-props": r"'required' : false"
                   },
                   {"field": 'remarks',
                   'max_length':150,
                   "data-dojo-type": "dijit.form.Textarea",
                    "data-dojo-props": r"'required' : false"
                   }
          ]
    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['max_length'] = field['max_length']

