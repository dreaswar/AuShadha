from django.conf.urls.defaults import *

import AuShadha.settings

from patient.views import *
from patient.medication_list import *
from patient.family_history import *
from patient.immunisation import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',


#################### PATIENT ###############################

  url(r'list/$',
	'patient.views.render_patient_list'	,
	name = 'render_patient_list'
  ),
  url(r'search/$'	, 
      'patient.views.patient_search',
      name = "patient_search"
  ),
  (r'search/(?P<search_by>\w+)/(?P<search_for>\w+)/$'	, 
   'patient.views.patient_search'	
  ),
  url(r'new/add/$'								,
      'patient.views.patient_new_add',
      name = 'patient_new_add'	
   ),

  url(r'patient_filtering_search_json/$'	, 
      'patient.views.patient_filtering_search_json',
      name = "patient_filtering_search_json_without_id"
  ),

  url(r'patient_filtering_search_json/(?P<id>\d+)/$'	, 
      'patient.views.patient_filtering_search_json',
      name = "patient_filtering_search_json_with_id"
  ),

###########################################################################################

#    url(r'detail/(?P<id>\d+)/$',
#    		'patient.views.patient_detail_list',
#    		name = 'patient_detail_list'
#    ),

    url(r'detail/edit/(?P<id>\d+)/$',
    		'patient.views.patient_detail_edit',
    		name ='patient_detail_edit'
    ),
    url(r'detail/del/(?P<id>\d+)/$',
    		'patient.views.patient_detail_del',
    		name = 'patient_detail_del'
    ),

###########################################################################################

    url(r'contact/json/$',
    		'patient.views.contact_json',
    		name = 'contact_json'
    ),

#    url(r'contact/list/(?P<id>\d+)/$',
#    		'patient.views.patient_contact_list',
#    		name = 'patient_contact_list'
#    ),

    url(r'contact/add/(?P<id>\d+)/$',
    		'patient.views.patient_contact_add',
   		  name = 'patient_contact_add'
    ),
    url(r'contact/edit/(?P<id>\d+)/$',
    		'patient.views.patient_contact_edit',
    		name = 'patient_contact_edit'
    ),
    url(r'contact/del/(?P<id>\d+)/$',
    		'patient.views.patient_contact_del',
    		name = 'patient_contact_del'
    ),

###########################################################################################

    url(r'phone/json/$',
    		'patient.views.phone_json',
    		name = 'phone_json'
    ),

#    url(r'phone/list/(?P<id>\d+)/$',
#    		'patient.views.patient_phone_list',
#    		name = 'patient_phone_list'
#    ),

    url(r'phone/add/(?P<id>\d+)/$',
    		'patient.views.patient_phone_add',
    		name = 'patient_phone_add'
    ),
    url(r'phone/edit/(?P<id>\d+)/$',
    		'patient.views.patient_phone_edit',
    		name = 'patient_phone_edit'
    ),
    url(r'phone/del/(?P<id>\d+)/$',
    		'patient.views.patient_phone_del',
    		name = 'patient_phone_del'
    ),

###########################################################################################

#    url( r'email_and_fax/list/(?P<id>\d+)/$'           ,
#         'patient.views.patient_email_and_fax_list' ,
#         name = 'patient_email_and_fax_list' 
#    ),

    url( r'email_and_fax/add/(?P<id>\d+)/$'           , 
        'patient.views.patient_email_and_fax_add'  ,
        name = 'patient_email_and_fax_add'
    ),
    url( r'email_and_fax/edit/(?P<id>\d+)/$'           ,
        'patient.views.patient_email_and_fax_edit'  ,
        name = 'patient_email_and_fax_edit' 
    ),
    url( r'email_and_fax/del/(?P<id>\d+)/$'		, 
         'patient.views.patient_email_and_fax_del'	,
         name = 'patient_email_and_fax_del'
    ),

###########################################################################################

    url(r'guardian/json/$','patient.views.guardian_json',name = 'guardian_json' ),

#   url(r'guardian/list/(?P<id>\d+)/$', 'patient.views.patient_guardian_list',name = 'patient_guardian_list' ),

    url(r'guardian/add/(?P<id>\d+)/$','patient.views.patient_guardian_add',name = 'patient_guardian_add'   ),
    url(r'guardian/edit/(?P<id>\d+)/$','patient.views.patient_guardian_edit',name = 'patient_guardian_edit' ),
    url(r'guardian/del/(?P<id>\d+)/$','patient.views.patient_guardian_del',name = 'patient_guardian_del' ),


###########################################################################################

    url(r'demographics/json/$',
    		'patient.views.demographics_json',
    		name = 'demographics_json'
    ),

#    url(r'demographics/list/(?P<id>\d+)/$',
#    		'patient.views.patient_demographics_list',
#    		name = 'patient_demographics_list'
#    ),

    url(r'demographics/add/(?P<id>\d+)/$',
    		'patient.views.patient_demographics_add',
   		  name = 'patient_demographics_add'
    ),
    url(r'demographics/edit/(?P<id>\d+)/$',
    		'patient.views.patient_demographics_edit',
    		name = 'patient_demographics_edit'
    ),
    url(r'demographics/del/(?P<id>\d+)/$',
    		'patient.views.patient_demographics_del',
    		name = 'patient_demographics_del'
    ),

###########################################################################################


    url(r'social_history/json/$',
    		'patient.views.social_history_json',
    		name = 'social_history_json'
    ),

#    url(r'social_history/list/(?P<id>\d+)/$',
#    		'patient.social_history.patient_social_history_list',
#    		name = 'patient_social_history_list'
#    ),

    url(r'social_history/add/(?P<id>\d+)/$',
    		'patient.social_history.patient_social_history_add',
   		  name = 'patient_social_history_add'
    ),
    url(r'social_history/edit/(?P<id>\d+)/$',
    		'patient.social_history.patient_social_history_edit',
    		name = 'patient_social_history_edit'
    ),
    url(r'social_history/del/(?P<id>\d+)/$',
    		'patient.social_history.patient_social_history_del',
    		name = 'patient_social_history_del'
    ),

###########################################################################################

    url(r'allergies/json/$',
    		'patient.views.allergies_json',
    		name = 'allergies_json'
    ),

#    url(r'allergies/list/(?P<id>\d+)/$',
#    		'patient.views.patient_allergies_list',
#    		name = 'patient_allergies_list'
#    ),

    url(r'allergies/add/(?P<id>\d+)/$',
    		'patient.views.patient_allergies_add',
   		  name = 'patient_allergies_add'
    ),
    url(r'allergies/edit/(?P<id>\d+)/$',
    		'patient.views.patient_allergies_edit',
    		name = 'patient_allergies_edit'
    ),
    url(r'allergies/del/(?P<id>\d+)/$',
    		'patient.views.patient_allergies_del',
    		name = 'patient_allergies_del'
    ),

###########################################################################################

    url(r'family_history/json/$',
    		'patient.views.family_history_json',
    		name = 'family_history_json'
    ),

#    url(r'family_history/list/(?P<id>\d+)/$',
#    		'patient.family_history.patient_family_history_list',
#    		name = 'patient_family_history_list'
#    ),

    url(r'family_history/add/(?P<id>\d+)/$',
    		'patient.family_history.patient_family_history_add',
   		  name = 'patient_family_history_add'
    ),
    url(r'family_history/edit/(?P<id>\d+)/$',
    		'patient.family_history.patient_family_history_edit',
    		name = 'patient_family_history_edit'
    ),
    url(r'family_history/del/(?P<id>\d+)/$',
    		'patient.family_history.patient_family_history_del',
    		name = 'patient_family_history_del'
    ),

###########################################################################################


    url(r'social_history/json/$',
    		'patient.views.family_history_json',
    		name = 'social_history_json'
    ),

#    url(r'social_history/list/(?P<id>\d+)/$',
#    		'patient.social_history.patient_social_history_list',
#    		name = 'patient_social_history_list'
#    ),

#    url(r'social_history/add/(?P<id>\d+)/$',
#    		'patient.social_history.patient_social_history_add',
#   		  name = 'patient_social_history_add'
#    ),
#    url(r'social_history/edit/(?P<id>\d+)/$',
#    		'patient.social_history.patient_social_history_edit',
#    		name = 'patient_social_history_edit'
#    ),
#    url(r'social_history/del/(?P<id>\d+)/$',
#    		'patient.social_history.patient_social_history_del',
#    		name = 'patient_social_history_del'
#    ),

###########################################################################################

    url(r'immunisation/json/$',
    		'patient.views.immunisation_json',
    		name = 'immunisation_json'
    ),

#    url(r'immunisation/list/(?P<id>\d+)/$',
#    		'patient.immunisation.patient_immunisation_list',
#    		name = 'patient_immunisation_list'
#    ),

    url(r'immunisation/add/(?P<id>\d+)/$',
    		'patient.immunisation.patient_immunisation_add',
   		  name = 'patient_immunisation_add'
    ),
    url(r'immunisation/edit/(?P<id>\d+)/$',
    		'patient.immunisation.patient_immunisation_edit',
    		name = 'patient_immunisation_edit'
    ),
    url(r'immunisation/del/(?P<id>\d+)/$',
    		'patient.immunisation.patient_immunisation_del',
    		name = 'patient_immunisation_del'
    ),


###########################################################################################

    url(r'medication_list/json/$',
    		'patient.views.medication_list_json',
    		name = 'medication_list_json'
    ),

#    url(r'medication_list/list/(?P<id>\d+)/$',
#    		'patient.medication_list.patient_medication_list_list',
#    		name = 'patient_medication_list_list'
#    ),

    url(r'medication_list/add/(?P<id>\d+)/$',
    		'patient.medication_list.patient_medication_list_add',
   		  name = 'patient_medication_list_add'
    ),
    url(r'medication_list/edit/(?P<id>\d+)/$',
    		'patient.medication_list.patient_medication_list_edit',
    		name = 'patient_medication_list_edit'
    ),
    url(r'medication_list/del/(?P<id>\d+)/$',
    		'patient.medication_list.patient_medication_list_del',
    		name = 'patient_medication_list_del'
    ),


###########################################################################################

    url(r'admission/json/$','patient.views.admission_json',name = 'admission_json'  ),

#   url(r'admission/list/(?P<id>\d+)/$','patient.views.patient_admission_list', name = 'get_patient_admission_list'	 ),
    url( r'admission/add/(?P<id>\d+)/$'	,'patient.views.patient_admission_add',	name ='patient_admission_add'),
    url( r'admission/add/$','patient.views.patient_admission_add',name ='patient_admission_add'	),


    url(r'visit/json/$','patient.views.visit_json',name = 'visit_json' ),


    url(r'index/$', 'patient.views.patient_index', name='patient_index'),

    url(r'patient_id/autocompleter/$',	'patient.views.patient_id_autocompleter',name = 'patient_id_autocompleter'),
    url(r'patient_hospital_id/autocompleter/$',	'patient.views.hospital_id_autocompleter',name = 'patient_hospital_id_autocompleter'),
    url(r'patient_name/autocompleter/$'	,'patient.views.patient_name_autocompleter',name = 'patient_name_autocompleter'	),

)

