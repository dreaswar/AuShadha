######################
# Patient Models for managing patient contact, phone, email, and Guardian details
# Author; Dr. Easwar T R
# Date: 15 - Feb 2011
# Licence: GPL 3
########################

from django.db 							import models
from django.forms 					import ModelForm
from django.core.exceptions 	import ValidationError
from django 								import forms

from admission.models 			import *

#from dojango.forms import ModelForm

class PatientDetail(models.Model):

	'''
	Patient Detail Model that gives the models definition and the associated methods to control the Patient models.
	
	'''

	patient_hospital_id = models.CharField('Hospital ID',
																				 max_length =15, 
																				 null = True, 
																				 blank = True
															 )

	first_name 					= models.CharField(max_length =30)

	middle_name 				= models.CharField(max_length =30, 
																				 help_text = "Please enter Initials / Middle Name", 
																				 blank = True, 
																				 null = True
																)

	last_name 					=  models.CharField(max_length =30, 
																					blank = True, 
																					null = True, 
																					help_text= "Enter Initials / Last Name"
																)

	full_name 					= models.CharField(max_length =100, 
	                                       editable = False,
	                                       null     = False,
	                                       blank    = False
	                             )

	age 								= models.CharField(max_length =10, 
																				 blank = True, 
																				 null = True
															 )

	sex 								= models.CharField(max_length =6, 
																				 choices=(("Male","Male"),
																				 					("Female","Female"),
																				 					("Others","Others")
																				 ), 
																				 default = "Male"
															 )


## Define the Unicode method for Patient Detail Model::

	def __unicode__(self):
		if self.middle_name and self.last_name:
			return "%s %s %s" %(self.first_name.capitalize(), 
													self.middle_name.capitalize(), 
													self.last_name.capitalize()
												 )
		elif self.last_name:
			return "%s %s" %(self.first_name.capitalize(),
												self.last_name.capitalize()
											 )
		else:
			return "%s %s" %(self.first_name.capitalize(),
												self.middle_name.capitalize()
											 )

	def _set_full_name(self):
		if self.middle_name and self.last_name:
			self.full_name =  unicode(
			                   self.first_name.capitalize()+ " " +
												 self.middle_name.capitalize()+ " "+
												 self.last_name.capitalize()
												)

		elif self.last_name:
			self.full_name = unicode(self.first_name.capitalize()+ " " +
												       self.last_name.capitalize()
											 )
		else:
			self.full_name = unicode(self.first_name.capitalize()+ " "+
												self.middle_name.capitalize()
											 )
		return self.full_name


## Defines all the URLS associated with a Patient Model and the actions associated::    

	def get_patient_home_url(self):
		'''Returns the Home of the Patient with a specific ID. 
			 This is the place where the central actions of the Patient can be managed at one place.
			 This includes Contacts/ Admissions / OP visits etc..
		'''
		return '/ds/pat/home/%s/' %self.id

	def get_patient_main_window_url(self):
		'''
			Returns the Main Window URL for the Patient which allows editing of Patient details, visits, admission.
		'''
		return '/ds/pat/main_window/%s/' %self.id

################################################################################

	def get_patient_detail_list_url(self):
		'''
			Returns the Listing URL for the Patient which allows editing of Patient Contacts, Phone, Guardian etc..
		'''
		return '/ds/pat/detail/list/%s/' %self.id

	def get_patient_detail_edit_url(self):
		'''
			Returns the Editing URL for the Patient which allows editing of Patient Contacts, Phone, Guardian etc..
		'''
		return '/ds/pat/detail/edit/%s/' %self.id

	def get_patient_detail_del_url(self):
		'''
			Returns the Deleting URL for the Patient.
			This action will delete all details of the patient including the admission, visits, phy-exam records, media etc..
		'''
		return '/ds/pat/detail/del/%s/' %self.id

################################################################################

	def get_patient_contact_list_url(self):
		'''
			Returns the URL for Listing contact details for a Patient
		'''
		return '/ds/pat/contact/list/%s/' %self.id

	def get_patient_contact_add_url(self):
		'''
			Returns the URL for adding contact details for a Patient
		'''
		return '/ds/pat/contact/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_phone_list_url(self):
		'''
			Returns the URL for listing phone details for a Patient
		'''
		return '/ds/pat/phone/list/%s/' %self.id

	def get_patient_phone_add_url(self):
		'''
			Returns the URL for adding phone details for a Patient
		'''
		return '/ds/pat/phone/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_guardian_list_url(self):
		'''
			Returns the URL for List guardian details for a Patient
		'''
		return '/ds/pat/guardian/list/%s/' %self.id

	def get_patient_guardian_add_url(self):
		'''
			Returns the URL for adding guardian details for a Patient
		'''
		return '/ds/pat/guardian/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_email_and_fax_list_url(self):
		'''
			Returns the URL for list email and fax details for a Patient
		'''
		return '/ds/pat/email_and_fax/list/%s/' %self.id

	def get_patient_email_and_fax_add_url(self):
		'''
			Returns the URL for adding email and fax details for a Patient
		'''
		return '/ds/pat/email_and_fax/add/%s/' %self.id

################################################################################

################################################################################

	def get_patient_admission_list_url(self):
		'''
			Returns the URL for listing admissions for a Patient
		'''
		return '/ds/pat/admission/list/%s/' %self.id  

	def get_patient_admission_add_url(self):
		'''
			Returns the URL for adding admissions for a Patient
		'''
		return '/ds/pat/admission/add/%s/' %self.id  

	def get_patient_visit_list_url(self):
		'''
		Returns the URL for listing visits for a Patient
		'''
		return '/ds/visit/detail/list/%s/' %self.id    

	def get_patient_visit_add_url(self):
		'''
		Returns the URL for adding visit for a Patient
		'''
		return '/ds/visit/detail/add/%s/' %self.id    

################################################################################

################################################################################

	def allergy_add_url(self):
		'''
		Returns the URL for adding allergy for a Patient
		'''
		return '/ds/allergy/add/%s/' %self.id    

	def allergy_list_url(self):
		'''
		Returns the URL for listing allergy for a Patient
		'''
		return '/ds/allergy/list/%s/' %self.id    

################################################################################

## Defines all the methods associated with the Patient Model for manipulation and queriing..

	def check_before_you_add(self):
		'''
			Checks whether the patient has already been registered in the database before adding.
		'''
		all_pat = PatientDetail.objects.all()
		hosp_id = self.patient_hospital_id
		id_list = []
		if all_pat:
			for patient in all_pat:
				id_list.append(patient.patient_hospital_id)
				if hosp_id in id_list:
					error = "Patient is already registered" 
					return False,error
				else:
					return True
		else:
			return True

	def save(self,*args, **kwargs):
		check_result = self.check_before_you_add()
		if check_result:
			self._set_full_name()
			print "Created Patient:" , self.full_name
			super(PatientDetail, self).save(*args, **kwargs)
		else:
			raise forms.ValidationError(check_result)

	def has_active_admission(self):
		''' Queries whether a given patient has an active admission
				returns the string representation of the number of active admissions
				FIXME:: May be it is better to make it return a Boolean,
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
		''' Returns the number of admissions for a patient after calling has_active_admission.
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
			verbose_name 				= "Basic Data"
			verbose_name_plural = "Basic Data"
			ordering 						= ('first_name', 'middle_name','last_name','age','sex','patient_hospital_id')



class PatientGuardian(models.Model):

	'''
		Class that defines the Guardian of a Particular patient    
	'''

	guardian_name 				= models.CharField(max_length = 20, 
																					 blank 			= True, 
																					 null 			= True, 
																					 help_text 	=	"Enter Guardian Name if Patient is a minor"
																 )

	relation_to_guardian 	= models.CharField('Relation',
																					max_length 	=	20, 
																					blank 			= True, 
																					null 				= True, 
																					help_text 	= "Enter relationship to Guardian if Patient is a Minor", 
																					choices 		=(("Father","Father"),
																												("Mother","Mother"),
																												("Local Guardian","LocalGuardian")
																											 )
																	)

	guardian_phone 				= models.PositiveIntegerField('Phone',
																											max_length 	= 20, 
																											blank 			= True, 
																											null 				= True
																	)

	patient_detail 				= models.ForeignKey(PatientDetail, null = True, blank = True)

	def __unicode__(self):
		if self.guardian_name:
			return "%s "%(self.guardian_name)
		else:
			return "No Guardian Name Provided"

	class Meta:
		verbose_name 				= "Guardian Details"
		verbose_name_plural = "Guardian Details"
		ordering 						= ('patient_detail','guardian_name')

	def get_patient_guardian_edit_url(self):
		'''
			Returns the URL for editing Guardian details for a Patient
		'''
		return '/ds/pat/guardian/edit/%s/' %self.id

	def get_patient_guardian_del_url(self):
		'''
			Returns the URL for adding Guardian details for a Patient
		'''
		return '/ds/pat/guardian/del/%s/' %self.id


class PatientContact(models.Model):

	'''Class that defines the Contact Address of a particular patient
	'''

	address_type 		= models.CharField('Type',
																	max_length = 10, 
																	choices =(("Home", "Home"),
																					  ("Office","Office"),
																					  ("Others","Others")
																					 ), 
																	default = "Home"
																	)
	address 				= models.TextField(max_length = 100, help_text = 'limit to 100 words')
	city 						= models.CharField(max_length = 20,default = 'Coimbatore')
	state 					= models.CharField(max_length =20, default= "Tamil Nadu")
	country 				= models.CharField(max_length =20, default = "India")
	pincode 				= models.PositiveIntegerField(max_length =8, null = True, blank = True)
	patient_detail 	= models.ForeignKey(PatientDetail, null = True, blank = True)

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
		verbose_name 				= "Address"
		verbose_name_plural = "Address"
		ordering 						= ('patient_detail','city','state')

	def get_patient_contact_edit_url(self):
		'''
			Returns the URL for editing phone details for a Patient
		'''
		return '/ds/pat/contact/edit/%s/' %self.id

	def get_patient_contact_del_url(self):
		'''
			Returns the URL for adding phone details for a Patient
		'''
		return '/ds/pat/contact/del/%s/' %self.id


class PatientPhone(models.Model):
	'''
		Class that defines the Phone data of a patient
	'''
	phone_type 			= models.CharField('Type',
																			max_length = 10, 
																			choices =(("Home", "Home"),
																								("Office","Office"),
																								("Mobile","Mobile"),
																								("Fax","Fax"),
																								("Others","Others")
																							 ), 
																			default = "Home")
	ISD_Code 				= models.PositiveIntegerField('ISD',max_length = 4, 
	                                               null = True, blank = True, 
	                                               default = "0091"
	                                             )
	STD_Code 				= models.PositiveIntegerField('STD',max_length = 4, null = True, 
	                                              blank = True, default = "0422"
	                                             )
	phone 					= models.PositiveIntegerField(max_length = 10, null = True, blank = True)
	patient_detail 	= models.ForeignKey(PatientDetail, null = True, blank = True)

	class Meta:
		verbose_name 				= "Phone"
		verbose_name_plural = "Phone"
		ordering 						= ('patient_detail','phone_type','ISD_Code','STD_Code')

	def __unicode__(self):
		if self.phone:
			return "%s- %s -%s" %(self.ISD_Code, self.STD_Code, self.phone)
		else:
			return "No Phone Number Provided"


	def get_patient_phone_edit_url(self):
		'''
			Returns the URL for editing phone details for a Patient
		'''
		return '/ds/pat/phone/edit/%s/' %self.id

	def get_patient_phone_del_url(self):
		'''
			Returns the URL for adding phone details for a Patient
		'''
		return '/ds/pat/phone/del/%s/' %self.id



class PatientEmailFax(models.Model):
	''' 
		Model that manages the Email, Fax and Web contact details of a patient
	'''
	date_entered 		= models.DateTimeField(auto_now_add = True)
	email 					= models.EmailField(max_length = 75, blank = True, null = True)
	fax 						= models.PositiveIntegerField(max_length = 20, null = True, blank = True)
	web 						= models.URLField(max_length = 50, null = True, blank = True)
	patient_detail 	= models.ForeignKey(PatientDetail, null = True, blank = True)

	def __unicode__(self):
		return "%s- %s -%s" %(self.email, self.fax, self.web)

	class Meta:
		verbose_name 				= "Email, Web and Fax"
		verbose_name_plural = "Email, Web and Fax"
		ordering 						= ('date_entered','patient_detail')

	def get_patient_email_and_fax_edit_url(self):
		'''
			Returns the URL for editing Email details for a Patient
		'''
		return '/ds/pat/email_and_fax/edit/%s/' %self.id

	def get_patient_phone_del_url(self):
		'''
			Returns the URL for adding phone details for a Patient
		'''
		return '/ds/pat/email_and_fax/del/%s/' %self.id




## Modelform definition of Patients.

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
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'\\d{3}','invalidMessage' : 'Invalid Character'"
                   },
                   {"field"    : 'sex',
		                'max_length'    :  30         ,
                   "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' : 'true' ,'regExp':'','invalidMessage' : ''"
                   },
		              ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']

#		def initTextField(self,*args, **kwargs):
#			

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
