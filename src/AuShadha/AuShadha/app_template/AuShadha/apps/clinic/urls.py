from django.conf.urls import *

import AuShadha.settings

from patient.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',


                       # PATIENT ###############################

                       url(	r'/list/$'				,
                            'AuShadha.patient.views.render_patient_list'	,
                            name='render_patient_list'
                            ),

                       url(r'search/$'	,
                           'AuShadha.patient.views.patient_search',
                           name="patient_search"
                           ),

                      (r'search/(?P<search_by>\w+)/(?P<search_for>\w+)/$'	,
                       'AuShadha.patient.views.patient_search'
                       ),

                       url(r'new/add/$'								,
                           'AuShadha.patient.views.patient_new_add',
                           name='patient_new_add'
                           ),

                       #

                       #    url(r'detail/(?P<id>\d+)/$',
                       #    		'AuShadha.patient.views.patient_detail_list',
                       #    		name = 'patient_detail_list'
                       #    ),

                       url(r'detail/edit/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_detail_edit',
                           name='patient_detail_edit'
                           ),
                       url(r'detail/del/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_detail_del',
                           name='patient_detail_del'
                           ),

                       #

                       url(r'contact/json/$',
                           'AuShadha.patient.views.contact_json',
                           name='contact_json'
                           ),

                       #    url(r'contact/list/(?P<id>\d+)/$',
                       #    		'AuShadha.patient.views.patient_contact_list',
                       #    		name = 'patient_contact_list'
                       #    ),

                       url(r'contact/add/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_contact_add',
                           name='patient_contact_add'
                           ),
                       url(r'contact/edit/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_contact_edit',
                           name='patient_contact_edit'
                           ),
                       url(r'contact/del/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_contact_del',
                           name='patient_contact_del'
                           ),

                       #

                       url(r'phone/json/$',
                           'AuShadha.patient.views.phone_json',
                           name='phone_json'
                           ),

                       #    url(r'phone/list/(?P<id>\d+)/$',
                       #    		'AuShadha.patient.views.patient_phone_list',
                       #    		name = 'patient_phone_list'
                       #    ),

                       url(r'phone/add/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_phone_add',
                           name='patient_phone_add'
                           ),
                       url(r'phone/edit/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_phone_edit',
                           name='patient_phone_edit'
                           ),
                       url(r'phone/del/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_phone_del',
                           name='patient_phone_del'
                           ),

                       #

                       #    url( r'email_and_fax/list/(?P<id>\d+)/$'           ,
                       #         'AuShadha.patient.views.patient_email_and_fax_list' ,
                       #         name = 'patient_email_and_fax_list'
                       #    ),

                       url(r'email_and_fax/add/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_email_and_fax_add',
                           name='patient_email_and_fax_add'
                           ),
                       url(r'email_and_fax/edit/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_email_and_fax_edit',
                           name='patient_email_and_fax_edit'
                           ),
                       url(r'email_and_fax/del/(?P<id>\d+)/$'		,
                           'AuShadha.patient.views.patient_email_and_fax_del'	,
                           name='patient_email_and_fax_del'
                           ),

                       #

                       url(r'guardian/json/$',
                           'AuShadha.patient.views.guardian_json',
                           name='guardian_json'
                           ),

                       #    url(r'guardian/list/(?P<id>\d+)/$',
                       #    		'AuShadha.patient.views.patient_guardian_list',
                       #    		name = 'patient_guardian_list'
                       #    ),

                       url(r'guardian/add/(?P<id>\d+)/$'	,
                           'AuShadha.patient.views.patient_guardian_add',
                           name='patient_guardian_add'
                           ),
                       url(r'guardian/edit/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_guardian_edit',
                           name='patient_guardian_edit'
                           ),
                       url(r'guardian/del/(?P<id>\d+)/$',
                           'AuShadha.patient.views.patient_guardian_del',
                           name='patient_guardian_del'
                           ),


                       url(r'admission/json/$',
                           'AuShadha.patient.views.admission_json',
                           name='admission_json'
                           ),

                       #		url(r'admission/list/(?P<id>\d+)/$',
                       #		    'AuShadha.patient.views.patient_admission_list'	,
                       #		    name = 'get_patient_admission_list'
                       #    ),
                       url(r'admission/add/(?P<id>\d+)/$'	,
                           'AuShadha.patient.views.patient_admission_add',
                           name='patient_admission_add'
                           ),
                       url(r'admission/add/$'	,
                           'AuShadha.patient.views.patient_admission_add',
                           name='patient_admission_add'
                           ),

                       url(r'visit/json/$',
                           'AuShadha.patient.views.visit_json',
                           name='visit_json'
                           ),


                       url(r'index/$', 'ds.patient.views.patient_index',
                           name='patient_index'),

                       url(	r'patient_id/autocompleter/$'				,
                            'AuShadha.patient.views.patient_id_autocompleter'	,
                            name='patient_id_autocompleter'
                            ),

                       url(	r'patient_hospital_id/autocompleter/$'				,
                            'AuShadha.patient.views.hospital_id_autocompleter'	,
                            name='patient_hospital_id_autocompleter'
                            ),


                       url(	r'patient_name/autocompleter/$'				,
                            'AuShadha.patient.views.patient_name_autocompleter'	,
                            name='patient_name_autocompleter'
                            ),

                       )
