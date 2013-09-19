################################################################################
# PROJECT      : AuShadha
# Description  : Patient Models for managing patient 
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

from django.db import models
from django.contrib.auth.models import User

from utilities.urls import generic_url_maker
from clinic.models import Clinic
from aushadha_base_models.models import AuShadhaBaseModel,AuShadhaBaseModelForm
#from demographics.models import Contact, Phone, Guardian
from dijit_fields_constants import PATIENT_DETAIL_FORM_CONSTANTS

DEFAULT_PATIENT_DETAIL_FORM_EXCLUDES=('parent_clinic',)


class PatientDetail(AuShadhaBaseModel):

    """
      Patient Model definition for Registration, Name entry and Hospital ID Generation
    """

   # Some data to Generate the URLS

    __model_label__ = "patient"

    _parent_model = 'parent_clinic'

    _can_add_list_or_json = [
                            'contact',
                            'phone',
                            'guardian',
                            'demographics',
                            'email_and_fax',

                            'admission',
                            'visit',

                            'medical_history',
                            'surgical_history',
                            'social_history',
                            'family_history',
                            'immunisation',
                            'obstetric_history_detail',

                            'medication_list',
                            'allergy_list'
                       ]
    _extra_url_actions = ['transfer_patient','transfer_clinic','refer']




    # Model attributes
    patient_hospital_id = models.CharField('Hospital ID',
                                           max_length=15, 
                                           null=True, 
                                           blank=True, 
                                           unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30,
                                   help_text="Please enter Initials / Middle Name",
                                   blank=True, 
                                   null=True)
    last_name = models.CharField(max_length=30, blank=True,
                                 null=True,
                                 help_text="Enter Initials / Last Name")
    full_name = models.CharField(max_length=100,
                                 editable=False,
                                 null=False,
                                 blank=False
                                 )
    age = models.CharField(max_length=10, blank=True, null=True)
    sex = models.CharField(max_length=6,
                           choices=(("Male", "Male"),
                                    ("Female", "Female"),
                                    ("Others", "Others")
                                    ),
                           default = "Male")
    parent_clinic = models.ForeignKey('clinic.Clinic')


    class Meta:
        verbose_name = "Patient - Basic Data"
        verbose_name_plural = "Patient - Basic Data"
        ordering = ('first_name', 
                    'middle_name',
                    'last_name', 
                    'age', 'sex', 
                    'patient_hospital_id'
                    )
        unique_together = ('patient_hospital_id', 'parent_clinic')

    def save(self, *args, **kwargs):
        """Custom Save Method needs to be defined.

        This should check for:
        1. Whether the patient is registered before.
        2. Patient DOB / Age Verfication and attribute setting
        3. Setting the full_name attribute

        """
        self.check_before_you_add()
        self._set_full_name()
    #     self._set_age()
        super(PatientDetail, self).save(*args, **kwargs)

    # Define the Unicode method for Patient Detail Model::
    def __unicode__(self):
        if self.middle_name and self.last_name:
            return "%s %s %s" % (self.first_name.capitalize(),
                                 self.middle_name.capitalize(),
                                 self.last_name.capitalize()
                                 )
        elif self.last_name or self.middle_name:
          if self.last_name:
            return "%s %s" % (self.first_name.capitalize(), self.last_name.capitalize())
          else:
            return "%s %s" % (self.first_name.capitalize(), self.middle_name.capitalize())

    def _field_list(self):
        self.field_list = []
        print self._meta.fields
        for field in self._meta.fields:
            self.field_list.append(field)
        return self.field_list

    def _formatted_obj_data(self):
        if not self.field_list:
            _field_list()
        str_obj = "<ul>"
        for obj in self._field_list:
            _str += "<li>" + obj + "<li>"
            str_obj += _str
        str_obj += "</ul>"
        return str_obj

# Defines and sets the Full Name for a Model on save.
# This stores the value under the self.full_name attribute.
# This is mainly intented for name display and search
    def _set_full_name(self):
        if self.middle_name and self.last_name:
            self.full_name = unicode(self.first_name.capitalize() + " " +
                                     self.middle_name.capitalize() + " " +
                                     self.last_name.capitalize()
                                     )
        else:
          if self.last_name:
            self.full_name = unicode(self.first_name.capitalize() + " " +
                                     self.last_name.capitalize()
                                     )
          if self.middle_name:
            self.full_name = unicode(self.first_name.capitalize() + " " +
                                     self.middle_name.capitalize()
                                     )
        return self.full_name

# Check DOB and Age. See Which one to set. Dont set age if DOB is given. Dont allow age > 120 to be set.
# This should be called before Form & Model save.
# If this returns false, the save should fail raising proper Exception
    def _set_age(self):
        if self.date_of_birth:
            min_allowed_dob = datetime.datetime(1900, 01, 01)
            max_allowed_dob = datetime.datetime.now()
            if self.date_of_birth >= min_allowed_dob and \
                self.date_of_birth <= max_allowed_dob:
                self.age = "%.2f" % (
                    round((max_allowed_dob - self.date_of_birth).days / 365.0, 2))
                return True
            else:
                raise Exception(
                    "Invalid Date: Date should be from January 01 1900 to Today's Date")
        else:
            if self.age and int(self.age[0:3]) <= 120:
                self.date_of_bith = None
                return True
            else:
                raise Exception("Invalid Date of Birth / Age Supplied")
                return False

    # Defines all the URLS associated with a Patient Model and the actions associated::

    #def get_patient_detail_list_url(self):
        #"""Returns the Listing URL for the Patient which allows editing of
        #Patient Contacts, Phone, Guardian etc.."""
        #return '/AuShadha/pat/detail/list/%s/' % self.id


    #def get_patient_contact_list_url(self):
        #"""Returns the URL for Listing contact details for a Patient."""
        #return '/AuShadha/pat/contact/list/%s/' % self.id

    #def get_patient_contact_add_url(self):
        #"""Returns the URL for adding contact details for a Patient."""
        #return '/AuShadha/pat/contact/add/%s/' % self.id


    #def get_patient_phone_list_url(self):
        #"""Returns the URL for listing phone details for a Patient."""
        #return '/AuShadha/pat/phone/list/%s/' % self.id

    #def get_patient_phone_add_url(self):
        #"""Returns the URL for adding phone details for a Patient."""
        #return '/AuShadha/pat/phone/add/%s/' % self.id

    #def get_patient_guardian_list_url(self):
        #"""Returns the URL for List guardian details for a Patient."""
        #return '/AuShadha/pat/guardian/list/%s/' % self.id

    #def get_patient_guardian_add_url(self):
        #"""Returns the URL for adding guardian details for a Patient."""
        #return '/AuShadha/pat/guardian/add/%s/' % self.id

    #def get_patient_email_and_fax_list_url(self):
        #"""Returns the URL for list email and fax details for a Patient."""
        #return '/AuShadha/pat/email_and_fax/list/%s/' % self.id

    #def get_patient_email_and_fax_add_url(self):
        #"""Returns the URL for adding email and fax details for a Patient."""
        #return '/AuShadha/pat/email_and_fax/add/%s/' % self.id


    #def get_patient_demographics_data_list_url(self):
        #"""Returns the Demographics details for a Patient."""
        #return '/AuShadha/pat/demographics/list/%s/' % self.id

    #def get_patient_demographics_data_add_url(self):
        #"""Returns the URL for adding Demographics details for a Patient."""
        #return '/AuShadha/pat/demographics/add/%s/' % self.id

    #def get_patient_family_history_list_url(self):
        #"""Returns the Family History details for a Patient."""
        #return '/AuShadha/pat/family_history/list/%s/' % self.id

    #def get_patient_family_history_add_url(self):
        #"""Returns the URL for adding family History details for a Patient."""
        #return '/AuShadha/pat/family_history/add/%s/' % self.id


    #def get_patient_social_history_list_url(self):
        #"""Returns the Social History details for a Patient."""
        #return '/AuShadha/pat/social_history/list/%s/' % self.id

    #def get_patient_social_history_add_url(self):
        #"""Returns the URL for adding Social History details for a Patient."""
        #return '/AuShadha/pat/social_history/add/%s/' % self.id


    #def get_patient_medical_history_list_url(self):
        #"""Returns the Medical History details for a Patient."""
        #return '/AuShadha/pat/medical_history/list/%s/' % self.id

    #def get_patient_medical_history_add_url(self):
        #"""Returns the URL for adding Medical History details for a Patient."""
        #return '/AuShadha/pat/medical_history/add/%s/' % self.id


    #def get_patient_surgical_history_list_url(self):
        #"""Returns the Surgical history details for a Patient."""
        #return '/AuShadha/pat/surgical_history/list/%s/' % self.id

    #def get_patient_surgical_history_add_url(self):
        #"""Returns the URL for adding Surgical History details for a
        #Patient."""
        #return '/AuShadha/pat/surgical_history/add/%s/' % self.id

    #def get_patient_obstetric_history_detail_list_url(self):
        #"""Returns the Social Obstetric details for a Patient."""
        #return '/AuShadha/pat/obstetric_history_detail/list/%s/' % self.id

    #def get_patient_obstetric_history_detail_add_url(self):
        #"""Returns the URL for adding Obstetric History details for a
        #Patient."""
        #return '/AuShadha/pat/obstetric_history_detail/add/%s/' % self.id


    #def get_patient_medication_list_list_url(self):
        #"""Returns the Medication details for a Patient."""
        #return '/AuShadha/pat/medication_list/list/%s/' % self.id

    #def get_patient_medication_list_add_url(self):
        #"""Returns the URL for adding Medication List details for a Patient."""
        #return '/AuShadha/pat/medication_list/add/%s/' % self.id

    #def get_patient_immunisation_list_url(self):
        #"""Returns the Immnunisation details for a Patient."""
        #return '/AuShadha/pat/immunisation/list/%s/' % self.id

    #def get_patient_immunisation_add_url(self):
        #"""Returns the URL for adding Immunisation details for a Patient."""
        #return '/AuShadha/pat/immunisation/add/%s/' % self.id

    #def get_patient_allergies_add_url(self):
        #"""Returns the URL for adding allergy for a Patient."""
        #return '/AuShadha/pat/allergies/add/%s/' % self.id

    #def get_patient_allergies_list_url(self):
        #"""Returns the URL for listing allergy for a Patient."""
        #return '/AuShadha/pat/allergies/list/%s/' % self.id


    #def get_patient_admission_list_url(self):
        #"""Returns the URL for listing admissions for a Patient."""
        #return '/AuShadha/pat/admission/list/%s/' % self.id

    #def get_patient_admission_add_url(self):
        #"""Returns the URL for adding admissions for a Patient."""
        #return '/AuShadha/pat/admission/add/%s/' % self.id

    #def get_patient_visit_list_url(self):
        #"""Returns the URL for listing visits for a Patient."""
        #return '/AuShadha/visit/detail/list/%s/' % self.id

    #def get_patient_visit_add_url(self):
        #"""Returns the URL for adding visit for a Patient."""
        #return '/AuShadha/visit/detail/add/%s/' % self.id

    #def get_patient_visit_tree_url(self):
        #"""Returns the URL for listing visits for a Patient."""
        #return '/AuShadha/render_visit_tree/?patient_id=%s/' % self.id


    ## Defines all the methods associated with the Patient Model for
    ## manipulation and queriing..
    def check_before_you_add(self):
        """Checks whether the patient has already been registered in the
        database before adding."""
        all_pat = PatientDetail.objects.all()
        hosp_id = self.patient_hospital_id
        id_list = []
        if all_pat:
            for patient in all_pat:
                id_list.append(patient.patient_hospital_id)
                if hosp_id in id_list:
                    #raise Exception("Patient Already Registered")
                    error = "Patient is already registered"
                    return False, error
                else:
                    return True
        else:
            return True

    def has_active_admission(self):
        """Queries whether a given patient has an active admission."""
        from admission.models import Admission
        id = self.id
        try:
            pat_obj = PatientDetail.objects.get(pk=id)
        except(TypeError, ValueError, PatientDetail.DoesNotExist):
            return False
        adm_obj = Admission.objects.filter(
            patient_detail=pat_obj).filter(admission_closed=False)
        if adm_obj:
            return True
        else:
            return False

    def adm_for_pat(self):
        """Returns the number of admissions for a patient after calling
        has_active_admission.

        If no admission it returns the None. Useful for Templates
        manipulation.

        """
        from admission.models import Admission
        id = self.id
        try:
            pat_obj = PatientDetail.objects.get(pk=id)
        except(TypeError, ValueError, PatientDetail.DoesNotExist):
            return False
        if self.has_active_admission() == '0':
            return None
        else:
            all_adm_obj = Admission.objects.filter(patient_detail=pat_obj)
            return all_adm_obj

    def has_active_visit(self):
        """Queries whether a given patient has a active visit.

        Returns Boolean. Returns False in case of error.

        """

        from visit.models import VisitDetail
        id = self.id
        try:
            pat_obj = PatientDetail.objects.get(pk=id)
        except(TypeError, ValueError, AttributeError, PatientDetail.DoesNotExist):
            return False
        visit_obj = VisitDetail.objects.filter(
            patient_detail=pat_obj, is_active=True)
        if visit_obj:
            return True
        else:
            return False

    def can_add_new_visit(self):
        from visit.models import VisitDetail
        from admission.models import Admission
        id = self.id
        try:
            pat_obj = PatientDetail.objects.get(pk=id)
        except(TypeError, ValueError, AttributeError, PatientDetail.DoesNotExist):
            return False
        # if not self.has_active_visit():
        if not self.has_active_admission():
            return True
        else:
            return False
        # else:
            # return False


    def visit_for_pat(self):
        """Details the visit details for each patient.

        This is useful for display on the Patient List table in
        template. Can just call this method and format a table with
        results for a quick view. Can use the return value of "Visit
        Object" to call the is_visit_active method if needed

        """

        from visit.models import VisitDetail
        id = self.id
        try:
            pat_obj = PatientDetail.objects.get(pk=id)
        except (TypeError, ValueError, AttributeError, PatientDetail.DoesNotExist):
            return False
        visit_obj = VisitDetail.objects.filter(patient_detail=pat_obj)
        if not visit_obj:
            return None
        else:
            return visit_obj


    #def get_patient_complaints(self):
        ##from django.utils import simplejson
        #from visit.models import VisitDetail, VisitComplaint
        #p_id = self.id
        #try:
            #pat_obj = PatientDetail.objects.get(pk=p_id)
        #except(TypeError, AttributeError, NameError):
            #raise Exception("Invalid ID. Raised Error")
        #except(PatientDetail.DoesNotExist):
            #raise Exception("Invalid Patient. No Such Patient on record")
        #visit_obj = VisitDetail.objects.filter(
            #patient_detail=pat_obj).order_by('-visit_date')
        #visit_complaint_list = []
        #if visit_obj:
            #for visit in visit_obj:
                #visit_complaints = VisitComplaint.objects.filter(
                    #visit_detail=visit)
                #if visit_complaints:
                    #for complaint in visit_complaints:
                        #dict_to_append = {}
                        #dict_to_append['complaint'] = complaint.complaint
                        #dict_to_append['duration'] = complaint.duration
                        #dict_to_append[
                            #'visit_date'] = complaint.visit_detail.visit_date.date().isoformat()
                        #dict_to_append[
                            #'is_active'] = complaint.visit_detail.is_active
                        #dict_to_append['visit_detail'] = complaint.visit_detail
                        #dict_to_append[
                            #'visit_fu'] = complaint.visit_detail.has_fu_visits()
                        #visit_complaint_list.append(dict_to_append)
        ##json = simplejson.dumps(visit_complaint_list)
        ## return json
        #return visit_complaint_list


    #def has_contact(self):
        #"""Returns a Boolean whether a particular patient has a contact or not
        #in Database."""
        #id = self.id
        #try:
            #pat_obj = PatientDetail.objects.get(pk=id)
        #except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
            #return False
        #contact = Contact.objects.filter(patient_detail=pat_obj)
        #if contact:
            #return contact
        #else:
            #return False

    #def has_phone(self):
        #"""Returns a Boolean whether a particular patient has a contact or not
        #in Database."""
        #id = self.id
        #try:
            #pat_obj = PatientPhone.objects.get(pk=id)
        #except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
            #return False
        #phone = Phone.objects.filter(patient_detail=pat_obj)
        #if phone:
            #return phone
        #else:
            #return False

    #def has_guardian(self):
        #"""Returns a Boolean whether a particular patient has a contact or not
        #in Database."""
        #id = self.id
        #try:
            #pat_obj = PatientDetail.objects.get(pk=id)
        #except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
            #return False
        #guardian = Guardian.objects.filter(patient_detail=pat_obj)
        #if guardian:
            #return guardian
        #else:
            #return False




class PatientDetailForm(AuShadhaBaseModelForm):

    """
        ModelForm for Patient Basic Data
    """

    __form_name__ = "Patient Detail Form"

    dijit_fields = PATIENT_DETAIL_FORM_CONSTANTS

    class Meta:
        model = PatientDetail
        exclude = DEFAULT_PATIENT_DETAIL_FORM_EXCLUDES
