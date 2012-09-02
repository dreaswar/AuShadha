##############################################################################
# Admission Models for AuShadha
# Takes care of all the admission related activities.
# Author    : Dr.Easwar T.R
# Date      : 27-02-2012
# Licence   : GNU GPL version3 Please see AuShadha/LICENSE.txt for the License
##############################################################################


from  django.db      import models
from  django.forms   import ModelForm
from  django.forms.widgets import Widget, Input

from  django.forms   import ValidationError
from  django.forms   import ModelForm, Textarea, CharField,Widget, TextInput, HiddenInput

from django.utils.safestring import mark_safe
from django.utils.encoding   import StrAndUnicode, force_unicode
from django.forms.util       import flatatt, to_current_timezone

from  patient.models 		import *
from  physician.models 		import *


import datetime

IMAGING_CHOICES = (	('MRI', 'MRI'), ('X-Ray', 'X-Ray'), ('USG', 'USG'), ('CT', 'CT'),('Others', 'Others'	) )



class Admission(models.Model):
		'''
		 Model to managed the admissions for a particular patient.
		 Describes the data to hold and the methods to use.
		'''
		date_of_admission   = models.DateField(auto_now = False)
		time_of_admission   = models.TimeField(auto_now = False)
		clinic              = models.CharField(max_length = 30, default = "Ortho One")
		room_or_ward        = models.CharField(max_length = 30, blank = True, null =True)
		patient_detail      = models.ForeignKey('patient.PatientDetail')
		admitting_physician = models.ForeignKey('physician.PhysicianDetail', related_name = 'admitting_physician')
		admission_closed    = models.BooleanField()
		created_at	    = models.DateTimeField(auto_now_add = True, editable = False)

		#TODO: admission_owner= models.ForeignKey('django.auth.models.User')

		class Meta:
			verbose_name		= "Admission Basic Data"
			verbose_name_plural	= "Admission Basic Data"
			ordering		= ('date_of_admission','time_of_admission', 'patient_detail', 'admitting_physician')

		def __unicode__(self):
			return "%s ,Pat:%s, Phy: %s" %(self.date_of_admission, self.patient_detail, self.admitting_physician)

################################################################################

		def get_admission_main_window_url(self):
			'''
			Returns the URL of the Admission Main Window.
			'''
			return '/AuShadha/admission/main_window/%s/' %(self.id)

		def get_admission_tree_json_url(self):
			'''
			Returns the URL of the Admission Tree.
			'''
			return '/AuShadha/admission/tree/json/%s/' %(self.id)


		def get_admission_detail_list_url(self):
			'''
			Returns the URL of the Admission Detail List Page.
			'''
			return '/AuShadha/admission/detail/list/%s/' %(self.id)

		def get_admission_detail_edit_url(self):
			'''
			Returns the URL of the Admission Detail Edit Page.
			'''
			return '/AuShadha/admission/detail/edit/%s/' %(self.id)

		def get_admission_detail_del_url(self):
			'''
			Returns the URL of the Admission Detail Delete Page.
			'''
			return '/AuShadha/admission/detail/del/%s/' %(self.id)


################################################################################

		def get_absolute_url(self):
			'''
			Returns the URL of the Admission Home.
			This webpage will handle all the current admission related events.

			'''
			return '/AuShadha/admission/home/%s/' %(self.id)

		def get_admission_edit_url(self):
			'''
			Returns the URL of the Admission Edit Page.

			'''
			return '/AuShadha/admission/edit/%s/' %(self.id)

		def get_admission_del_url(self):
			'''
			Returns the URL of the Admission Delete Page.

			'''
			return '/AuShadha/admission/del/%s/' %(self.id)


#################################################################################

		def get_phy_exam_main_window(self):
			'''
			Returns the URL of the Physical Examination List for this admission.

			'''
			return '/AuShadha/phy_exam/main_window/ip/%s/' %(self.id)

		def get_admission_phy_exam_list_url(self):
			'''
			returns the URL list all Physical Examination for the admission
			'''
			from ds.phyexam.models import PhyExam
			adm_obj   = Admission.objects.get(pk = self.id)
			phy_exam  = PhyExam.objects.filter(admission_detail = adm_obj)
			if len(phy_exam) >0:
				return "/AuShadha/admission/phy_exam/list/%s/" %(self.id)
			else:
				return "/AuShadha/admission/phy_exam/add/initial/%s/" %(self.id)

		def get_admission_phy_exam_start_url(self):
			'''
			returns the URL add Physical Examination
			'''
			from ds.phyexam.models import PhyExam
			adm_obj   = Admission.objects.get(pk = self.id)
			phy_exam  = PhyExam.objects.filter(admission_detail = adm_obj)
			if len(phy_exam) == 0:
				return "/AuShadha/admission/phy_exam/add/initial/%s/" %(self.id)
			elif len(phy_exam) >0:
				return "/AuShadha/admission/phy_exam/add/fu/%s/" %(self.id)

		def get_admission_phy_exam_add_fu_exam_url(self):
			'''
			returns the URL add Physical Examination
			'''
			return "/AuShadha/admission/phy_exam/add/fu/%s/" %(self.id)

		def get_admission_phy_exam_add_pre_op_exam_url(self):
			'''
			returns the URL add Preop Physical Examination
			'''
			return "/AuShadha/admission/phy_exam/add/pre_op/%s/" %(self.id)

		def get_admission_phy_exam_add_post_op_exam_url(self):
			'''
			returns the URL add Postop Physical Examination
			'''
			return "/AuShadha/admission/phy_exam/add/post_op/%s/" %(self.id)

		def get_admission_phy_exam_add_discharge_exam_url(self):
			'''
			returns the URL add Physical Examination
			'''
			return "/AuShadha/admission/phy_exam/add/discharge/%s/" %(self.id)


################################################################################

		def incidentreport_ip_list(self):
			'''
				Manages the Incidents for a particular Admission.
			'''
			return '/AuShadha/admission/incident/list/%s/' %(self.id)

		def incidentreport_ip_add(self):
			'''
				Adds Incidents for a particular Admission.
			'''
			return '/AuShadha/admission/incident/add/%s/' %(self.id)

################################################################################

		def get_admission_discharge_add_url(self):
			'''
			Returns the URL to Discharge an Admission.

			'''
			return '/AuShadha/admission/discharge/add/%s/' %(self.id)

################################################################################


		def get_admission_complaint_list_url(self):
			'''
			Returns the URL to list the admission complaints.

			'''
			return '/AuShadha/admission/complaints/list/%s/' %(self.id)

		def get_admission_complaint_add_url(self):
			'''
			Returns the URL to add new admission complaints.

			'''
			return '/AuShadha/admission/complaints/add/%s/' %(self.id)


################################################################################

################################################################################
		def get_admission_hpi_list_url(self):
			'''
			Returns the URL to list the admission HPI.

			'''
			return '/AuShadha/admission/hpi/list/%s/' %(self.id)

		def get_admission_hpi_add_url(self):
			'''
			Returns the URL to add new admission HPI.

			'''
			return '/AuShadha/admission/hpi/add/%s/' %(self.id)


################################################################################

################################################################################
		def get_admission_past_history_list_url(self):
			'''
			Returns the URL to list the admission past history.

			'''
			return '/AuShadha/admission/past_history/list/%s/' %(self.id)

		def get_admission_past_history_add_url(self):
			'''
			Returns the URL to add new admission past history.

			'''
			return '/AuShadha/admission/past_history/add/%s/' %(self.id)


################################################################################

################################################################################
		def get_admission_inv_list_url(self):
			'''
			Returns the URL to list the admission Investigations.

			'''
			return '/AuShadha/admission/inv/list/%s/' %(self.id)

		def get_admission_inv_add_url(self):
			'''
			Returns the URL to add new admission Investigations.

			'''
			return '/AuShadha/admission/inv/add/%s/' %(self.id)


################################################################################

################################################################################
		def get_admission_imaging_list_url(self):
			'''
			Returns the URL to list the admission Imaging.

			'''
			return '/AuShadha/admission/imaging/list/%s/' %(self.id)

		def get_admission_imaging_add_url(self):
			'''
			Returns the URL to add new admission Imaging.

			'''
			return '/AuShadha/admission/imaging/add/%s/' %(self.id)


################################################################################

################################################################################
		def get_admission_procedure_list_url(self):
			'''
			Returns the URL to list the admission Procedures.

			'''
			return '/AuShadha/admission/procedure/list/%s/' %(self.id)

		def get_admission_procedure_add_url(self):
			'''
			Returns the URL to add new admission Procedures.

			'''
			return '/AuShadha/admission/procedure/add/%s/' %(self.id)


################################################################################


		def has_phy_exam(self):
			''' Returns whether a chosen Admission Object has already a Physical Exam Recorded for Discharge Summary '''

			from phyexam.models import PhyExam
			id = self.id
			try:
				adm_object = Admission.objects.get(pk = id)
			except (TypeError, ValueError, AttributeError, Admission.DoesNotExist):
				return False
			phy_exam_object = PhyExam.objects.filter(admission_detail = adm_object)
			phy_exam_count  = unicode(len(phy_exam_object))
			if phy_exam_object == True:
				return phy_exam_count
			else:
				phy_exam_count == '0'
				return phy_exam_count



		def has_complaints(self):
			id              = self.id
			adm_obj         = Admission.objects.get(pk = id)
			adm_complaints  = AdmissionComplaint.objects.filter(admission_detail = adm_obj)
			if adm_complaints:
				return True
			else:
				return False


		def complaints_for_adm(self):
			id      = self.id
			adm_obj = Admission.objects.get(pk = id)
			if not adm_obj.has_complaints():
				return None
			else:
				adm_complaint_obj = AdmissionComplaint.objects.filter(admission_detail = adm_obj)
				return adm_complaint_obj

		def has_hpi(self):
			id              = self.id
			adm_obj         = Admission.objects.get(pk = id)
			adm_hpi  	= AdmissionHPI.objects.filter(admission_detail = adm_obj)
			if adm_hpi:
				return True
			else:
				return False

		def has_past_history(self):
			id             	  = self.id
			adm_obj        	  = Admission.objects.get(pk = id)
			adm_past_history  = AdmissionPastHistory.objects.filter(admission_detail = adm_obj)
			if adm_past_history:
				return True
			else:
				return False

		def has_diag(self):
			id 		= self.id
			try:
				adm_obj	= Admission.objects.get(pk = id)
			except (TypeError, AttributeError, ValueError):
				return None
			except (Admission.DoesNotExist):
				return False
			adm_diag_obj	= AdmissionDiagnosis.objects.filter(admission_detail = adm_obj)
			if adm_diag_obj:
				return True
			else:
				return False

		def has_imaging(self):
			id              = self.id
			adm_obj         = Admission.objects.get(pk = id)
			adm_imaging  	= AdmissionImaging.objects.filter(admission_detail = adm_obj)
			if adm_imaging:
				return True
			else:
				return False

		def has_inv(self):
			id              = self.id
			adm_obj         = Admission.objects.get(pk = id)
			adm_inv         = AdmissionInv.objects.filter(admission_detail = adm_obj)
			if adm_inv:
				return True
			else:
				return False

		def has_exam_on_admission(self):
			from phyexam.models import PhyExam
			id = self.id
			try:
				adm_obj = Admission.objects.get(pk = id)
			except (TypeError, ValueError, AttributeError, Admission.DoesNotExist):
				return False
			phy_exam_obj = PhyExam.objects.filter(admission_detail = adm_obj).filter(consult_nature = 'initial')
			if phy_exam_obj:
				return True
			else:
				return False

		def has_exam_on_preop(self):
			from phyexam.models import PhyExam
			id = self.id
			try:
				adm_obj = Admission.objects.get(pk = id)
			except (TypeError, ValueError, AttributeError, Admission.DoesNotExist):
				return False
			if self.has_phy_exam() != '0':
				phy_exam_obj = PhyExam.objects.filter(admission_detail = adm_obj).filter(consult_nature = 'pre_op')
				if phy_exam_obj:
					return True
				else:
					return False
			else:
				return False

		def has_exam_on_postop(self):
			from phyexam.models import PhyExam
			id = self.id
			try:
				adm_obj = Admission.objects.get(pk = id)
			except (TypeError, ValueError, AttributeError, Admission.DoesNotExist):
				return False
			if self.has_phy_exam() != '0':
				phy_exam_obj = PhyExam.objects.filter(admission_detail = adm_obj).filter(consult_nature = 'post_op')
				if phy_exam_obj:
					return True
				else:
					return False
			else:
				return False


		def has_exam_on_discharge(self):
			from phyexam.models import PhyExam
			id = self.id
			try:
				adm_obj = Admission.objects.get(pk = id)
			except (TypeError, ValueError, AttributeError, Admission.DoesNotExist):
				return False
			if self.has_phy_exam() != '0':
				phy_exam_obj = PhyExam.objects.filter(admission_detail = adm_obj).filter(consult_nature = 'discharge')
				if phy_exam_obj:
					return True
				else:
					return False
			else:
				return False


		def get_admission_discharge(self):
			from discharge.models import DischargeDetail
			if self.admission_closed:
				id            = self.id
				discharge_obj = DischargeDetail.objects.filter(admission_detail = self)
				if discharge_obj:
					return discharge_obj[0]
				else:
					return discharge_obj
			else:
				return False


		def fit_for_discharge_check(self, user, date_of_discharge):
			'''
				Checks to see if the admission is fit for Discharge. Returns true if all checks pass
			'''
			if self.admission_closed == False:
				if user == self.admitting_surgeon:
					if date_of_discharge >= self.date_of_admission:
						if self.has_complaints() 		and \
							self.has_hpi() 		        and \
							self.has_past_history() 	and \
							self.has_inv() 			and \
							self.has_imaging() 		and \
							self.has_exam_on_admission() 	and \
							self.has_exam_on_discharge() 	and \
							self.has_diag():
								print 'SUCCESS !. All preconditions satisfied.. Can be discharged.'
								return True
						else:
							print 'ERROR!. Cannot Discharge. Some physical Examinations / history may be missing.'
							return False
					else:
						print 'ERROR!. Date of Admission and Date of Discharge. The latter has to be greater.'
						return False
				else:
					print 'ERROR!. The User attempting Discharge should be same as the Admitting surgeon.'
					return False
			else:
				print 'ERROR!. This admission has already been discahrged.'
				return False
################################################################################################

		def return_phy_exam_model_form(self,phy_exam_instance, consult_nature,request_post= False):
			print "Received request for Generating Physical Examination form.. evaluating..."
			from phyexam.models import PhyExam,                 \
			                           IP_Initial_PhyExamForm,  \
			                           IP_Fu_PhyExamForm,       \
			                           IP_Discharge_PhyExamForm,\
			                           IP_Pre_Op_PhyExamForm,   \
			                           IP_Post_Op_PhyExamForm
			adm_obj      = Admission.objects.get(pk = self.id)
			print "Admission & Patient Detail: ", adm_obj
			phy_exam_obj = PhyExam.objects.filter(admission_detail = adm_obj)
			print "Number of recorded physical examinations are: " , len(phy_exam_obj)
			if len( phy_exam_obj) == 0:
				phy_exam_instance.consult_nature = 'initial'
				if not request_post: return IP_Initial_PhyExamForm(instance = phy_exam_instance)
				else: return IP_Initial_PhyExamForm(request_post, instance = phy_exam_instance)
			elif len(phy_exam_obj) >0:
				print "The received Consult Nature is: ", consult_nature
				if consult_nature == 'fu':
					print "Generating Physical Examination for for Follow up examination...."
					if not request_post: 
						print 'Request received as GET'
						form = IP_Fu_PhyExamForm(instance = phy_exam_instance)
						print "Finished generating form..."
						return form
					else: 
						print 'Request received as POST'
						form = IP_Fu_PhyExamForm(request_post, instance = phy_exam_instance)
						return form
				elif consult_nature == 'pre_op':
					if not request_post: 
						form = IP_Pre_Op_PhyExamForm(instance = phy_exam_instance)
						return form
					else: 
						return IP_Pre_Op_PhyExamForm(request_post, instance = phy_exam_instance)
				elif consult_nature == 'post_op':
					if not request_post:
						return IP_Post_Op_PhyExamForm(instance = phy_exam_instance)
					else:
						return IP_Post_Op_PhyExamForm(request_post, instance = phy_exam_instance)
				elif consult_nature == 'discharge' :
					if not request_post:
						return IP_Discharge_PhyExamForm(instance = phy_exam_instance)
					else:
						return IP_Discharge_PhyExamForm(request_post, instance = phy_exam_instance)
			else:
				raise Exception("Form Generation failed.....")

#FIXME: THIS CAN BE MADE ENDLESSLY COMPLEX WITH LOGIC OF WHETHER TO ADD
#        PHYSICAL EXAM AFTER DISCHARGE.. CHECKING WHETHER
#        DISCHARGE, PRE_OP,POST_OP EXAMS ARE PRESENT ...ETC...

################################################################################################

## TODO... Privileges..

		def admission_owner(self):
			'''
			Yeilds the Admitting Physician object.
			Only this Surgeon has the power to modify the Admission Details.
			'''
			id        = self.id
			physician = self.admitting_physician



################################################################################################

class AdmissionComplaint(models.Model):
	complaints        = models.CharField(max_length = 30, help_text= 'limit to 30 words')
	duration       	  = models.CharField(max_length = 30, help_text= 'limit to 30 words')
	admission_detail  = models.ForeignKey(Admission)
	created_at	  = models.DateTimeField(auto_now_add = True, editable = False)

	def __unicode__(self):
		return '%s : %s' %(self.complaints, self.duration)

	def get_admission_complaint_edit_url(self):
		return '/AuShadha/admission/complaints/edit/%s/' %(self.id)

	def get_admission_complaint_del_url(self):
		return '/AuShadha/admission/complaints/del/%s/' %(self.id)

	class Meta:
		verbose_name		= "Presenting Complaints"
		verbose_name_plural	= "Presenting Complaints"
		ordering		= ('admission_detail', 'created_at', 'complaints')


class AdmissionHPI(models.Model):
	hpi 			= models.TextField('History of Presenting Illness', max_length = 1000, help_text = 'limit to 1000 words')
	admission_detail 	= models.ForeignKey(Admission)
	created_at		= models.DateTimeField(auto_now_add = True, editable = False)

	def __unicode__(self):
		return '%s' %(self.hpi)

	def get_admission_hpi_edit_url(self):
		return '/AuShadha/admission/hpi/edit/%s/' %(self.id)

	def get_admission_hpi_del_url(self):
		return '/AuShadha/admission/hpi/del/%s/' %(self.id)

	class Meta:
		unique_together		= ('hpi', 'admission_detail')
		verbose_name		= "History of Presenting Illness"
		verbose_name_plural	= "History of Presenting Illness"
		ordering		= ('admission_detail', 'created_at', 'hpi')


class AdmissionPastHistory(models.Model):
	past_history 	   = models.TextField('Past History ', max_length = 1000, help_text = 'limit to 1000 words')
	admission_detail   = models.ForeignKey(Admission)
	created_at	   = models.DateTimeField(auto_now_add = True, editable = False)

	def __unicode__(self):
		return '%s' %(self.past_history)

	def get_admission_past_history_edit_url(self):
		return '/AuShadha/admission/past_history/edit/%s/' %(self.id)

	def get_admission_past_history_del_url(self):
		return '/AuShadha/admission/past_history/del/%s/' %(self.id)

	class Meta:
		unique_together		= ('past_history', 'admission_detail')
		verbose_name		= "Past History"
		verbose_name_plural     = "Past History"
		ordering		= ('admission_detail', 'created_at', 'past_history')


class AdmissionImaging(models.Model):
	modality	 = models.ForeignKey('inv_and_imaging.ImagingInvestigationRegistry')
	finding 	 = models.TextField('Finding', max_length = 1000, help_text = 'limit to 1000 words')
	admission_detail = models.ForeignKey(Admission)
	created_at	 = models.DateTimeField(auto_now_add = True, editable = True)

	def __unicode__(self):
		return '''%s: %s \n(%s)''' %(self.modality, self.finding, self.created_at.date().isoformat() )

	def __trimmed_unicode__(self):
		return '''%s: %s ... \n(%s)''' %(self.modality, self.finding[0:5], self.created_at.date().isoformat() )


#	def get_admission_imaging_add_url(self):
#		return '/AuShadha/admission/imaging/add/%s/' %(self.id)

	def get_admission_imaging_edit_url(self):
		return '/AuShadha/admission/imaging/edit/%s/' %(self.id)

	def get_admission_imaging_del_url(self):
		return '/AuShadha/admission/imaging/del/%s/' %(self.id)

	class Meta:
		verbose_name		= "Imaging Studies"
		verbose_name_plural     = "Imaging Studies"
		ordering		= ('admission_detail', 'created_at', 'modality')



class AdmissionInv(models.Model):
	investigation		= models.ForeignKey('inv_and_imaging.LabInvestigationRegistry')
	value 			= models.CharField('Findings', max_length = 30)
	admission_detail 	= models.ForeignKey(Admission)
	created_at		= models.DateTimeField(auto_now_add = True, editable = True)

	def __unicode__(self):
		return "%s: %s \n(%s)" %(self.investigation, self.value, self.created_at.date().isoformat())

	def get_admission_inv_edit_url(self):
		return '/AuShadha/admission/inv/edit/%s/' %(self.id)

	def get_admission_inv_del_url(self):
		return '/AuShadha/admission/inv/del/%s/' %(self.id)

	class Meta:
		verbose_name	       = "Lab Investigation"
		verbose_name_plural    = "Lab Investigation"
		ordering	       = ('admission_detail', 'created_at', 'investigation')




## Defines all the Model Forms for the Admission Model.
  
  #FIXME
  ## This has to be done elegantly. One way is to make it object oriented / use projects like DoJango. The other is to use
  ## Dojo.Behaviour to read regular HTML input tags and dijtise them

class AdmissionForm(ModelForm):

  class Meta:
    model = Admission
    exclude = ("admission_closed")

  def __init__(self, *args, **kwargs):
    super(AdmissionForm, self).__init__(*args, **kwargs)
    text_fields = [
                   {"field"         : 'patient_detail',
   		    'max_length'    :  ''         ,
		    "data-dojo-type": "dijit.form.Select",
		    "data-dojo-props": r"required:'true',readOnly:'true'"
	 	   },

                   {"field"           : 'date_of_admission',
		    'max_length'      :  ''         ,
		    "data-dojo-type"  : "dijit.form.DateTextBox",
		    "data-dojo-props" : r""
		   },

		   {"field"           : 'time_of_admission',
		    'max_length'      :  ''         ,
		    "data-dojo-type"  : "dijit.form.TimeTextBox",
		    "data-dojo-props" : r""
		   },

		  {"field"         : 'admitting_surgeon',
		   'max_length'    :  30         ,
		   "data-dojo-type": "dijit.form.Select",
		   "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z;:-_ ,.]+','invalidMessage' : 'Invalid Character'"
		  },
		  {"field"          : 'hospital',
		   'max_length'     : 30,
		   "data-dojo-type" : "dijit.form.ValidationTextBox",
		   "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z;:-_ ,.]+','invalidMessage' : 'Invalid Character'"
		  },
		  {"field"         : 'room_or_ward',
		   'max_length'    :  30         ,
		   "data-dojo-type": "dijit.form.ValidationTextBox",
		  "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
		  }		              
		]

    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['max_length']      = field['max_length']



class DojoDateTextBox(Input):
    """
    Base class for all DojoDateTextBox widgets 
    """
    input_type = 'text' # Subclasses must define this.
#    attrs      = {}
    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = datetime.datetime.now().isoformat()
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

class DojoTimeTextBox(Input):
  pass



class AdmissionEditForm(ModelForm):
  class Meta:
    model   = Admission
    widgets = {'patient_detail'			:TextInput(attrs={'readonly':'readonly'})}
    exclude = ( "admission_closed",)

class AdmissionComplaintForm(ModelForm):

  class Meta:
    model = AdmissionComplaint
#    widgets = {'admission_detail'			:TextInput(attrs={'readonly':'readonly'})}

  def __init__(self, *args, **kwargs):
    super(AdmissionComplaintForm, self).__init__(*args, **kwargs)
    text_fields = [
                   {"field"         : 'admission_detail',
   		   'max_length'     :  ''         ,
		   "data-dojo-type" : "dijit.form.Select",
		   "data-dojo-id"   : "admission_detail_complaint",
		   "data-dojo-props": r" 'required':'true', 'readOnly':'true'"
		  },
                  {"field"         : 'complaints',
		   'max_length'    :  '100'         ,
		   "data-dojo-type": "dijit.form.ValidationTextBox",
		   "data-dojo-id"  : "admission_complaint_complaints",
		   "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
		  },
		  {"field"         : 'duration',
		   'max_length'    :  '100'         ,
		   "data-dojo-type": "dijit.form.FilteringSelect",
		   "data-dojo-id"  : "admission_complaint_duration",
		   "data-dojo-props": r" name: 'duration',searchAttr:'id',store:complaintDurationsStore,required:'true', autoComplete:'false'"
		  },
		]

    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['data-dojo-id'] = field['data-dojo-id']
      self.fields[field['field']].widget.attrs['max_length']      = field['max_length']





class AdmissionHPIForm(ModelForm):

  class Meta:
    model = AdmissionHPI
  def __init__(self, *args, **kwargs):
    super(AdmissionHPIForm, self).__init__(*args, **kwargs)
    text_fields = [
                   {"field"         : 'admission_detail',
		'max_length'    :  ''         ,
		"data-dojo-type": "dijit.form.Select",
		"data-dojo-id"  : "admission_detail_hpi",
		"data-dojo-props": r" 'required':'true', 'readOnly':'true'"
		},
                {"field"         : 'hpi',
		'max_length'    :  '250'         ,
		"data-dojo-type": "dijit.form.SimpleTextarea",
		"data-dojo-id"  : "admission_hpi",
		"data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-_:0-9#]+','invalidMessage' : 'Invalid Character'"
		},
	      ]

    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['data-dojo-id'] = field['data-dojo-id']
      self.fields[field['field']].widget.attrs['max_length']      = field['max_length']


class AdmissionPastHistoryForm(ModelForm):

  class Meta:
    model = AdmissionPastHistory
#    widgets = {'admission_detail'			:TextInput(attrs={'readonly':'readonly'})}
  def __init__(self, *args, **kwargs):
    super(AdmissionPastHistoryForm, self).__init__(*args, **kwargs)
    text_fields = [
                   {"field"         : 'admission_detail',
		'max_length'    :  ''         ,
		"data-dojo-type": "dijit.form.Select",
		"data-dojo-id"  : "admission_detail_past_history",
		"data-dojo-props": r" 'required':'true', 'readOnly':'true'"
		},
               {"field"         : 'past_history',
		'max_length'    :  '1000'         ,
		"data-dojo-type": "dijit.form.SimpleTextarea",
		"data-dojo-id"  : "admission_past_history",
		"data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-_:0-9#]+','invalidMessage' : 'Invalid Character'"
		},
	      ]

    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['data-dojo-id']    = field['data-dojo-id']
      self.fields[field['field']].widget.attrs['max_length']      = field['max_length']


class AdmissionImagingForm(ModelForm):
	class Meta:
		model = AdmissionImaging
	def __init__(self, *args, **kwargs):
		super(AdmissionImagingForm, self).__init__(*args, **kwargs)
		text_fields = [
                   {"field"         : 'admission_detail',
		'max_length'    :  '100'         ,
		"data-dojo-type": "dijit.form.Select",
		"data-dojo-id"  : "admission_detail_investigation",
		"data-dojo-props": r" 'required':'true', 'readOnly':'true'"
		},

                   {"field"         : 'modality',
										'max_length'    :  '100'         ,
										"data-dojo-type": "dijit.form.Select",
										"data-dojo-id"  : "admission_imaging_imaging",
										"data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
										},

										{"field"         : 'finding',
										'max_length'    :  '1000'         ,
										"data-dojo-type": "dijit.form.SimpleTextarea",
										"data-dojo-id"  : "admission_imaging_finding",
										"data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
										},

									]

		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['data-dojo-id'] = field['data-dojo-id']
			self.fields[field['field']].widget.attrs['max_length']      = field['max_length']




class AdmissionInvForm(ModelForm):
	class Meta:
		model = AdmissionInv
	def __init__(self, *args, **kwargs):
		super(AdmissionInvForm, self).__init__(*args, **kwargs)
		text_fields = [
                   {"field"         : 'admission_detail',
										'max_length'    :  '100'         ,
										"data-dojo-type": "dijit.form.Select",
										"data-dojo-id"  : "admission_detail_investigation",
										"data-dojo-props": r" 'required':'true', 'readOnly':'true'"
										},

                   {"field"         : 'investigation',
										'max_length'    :  '100'         ,
										"data-dojo-type": "dijit.form.Select",
										"data-dojo-id"  : "admission_investigation_investigation",
										"data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
										},

										{"field"         : 'value',
										'max_length'    :  '100'         ,
										"data-dojo-type": "dijit.form.ValidationTextBox",
										"data-dojo-id"  : "admission_investigation_value",
										"data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
										},

									]

		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['data-dojo-id'] = field['data-dojo-id']
			self.fields[field['field']].widget.attrs['max_length']      = field['max_length']


