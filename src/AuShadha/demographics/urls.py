from django.conf.urls.defaults import *
from django.contrib import admin

import AuShadha.settings

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'contact/json/$',
                           'demographics.views.contact_json',
                           name='contact_json'
                           ),

                       #    url(r'contact/list/(?P<id>\d+)/$',
                       #    		'demographics.views.contact_list',
                       #    		name = 'patient_contact_list'
                       #    ),

                       url(r'contact/add/(?P<id>\d+)/$',
                           'demographics.views.contact_add',
                           name='contact_add'
                           ),
                       url(r'contact/edit/(?P<id>\d+)/$',
                           'demographics.views.contact_edit',
                           name='contact_edit'
                           ),
                       url(r'contact/del/(?P<id>\d+)/$',
                           'demographics.views.contact_del',
                           name='contact_del'
                           ),

                       url(r'phone/json/$',
                           'demographics.views.phone_json',
                           name='phone_json'
                           ),

                       #    url(r'phone/list/(?P<id>\d+)/$',
                       #    		'demographics.views.phone_list',
                       #    		name = 'phone_list'
                       #    ),

                       url(r'phone/add/(?P<id>\d+)/$',
                           'demographics.views.phone_add',
                           name='phone_add'
                           ),
                       url(r'phone/edit/(?P<id>\d+)/$',
                           'demographics.views.phone_edit',
                           name='phone_edit'
                           ),
                       url(r'phone/del/(?P<id>\d+)/$',
                           'demographics.views.phone_del',
                           name='phone_del'
                           ),

                       #    url( r'email_and_fax/list/(?P<id>\d+)/$'           ,
                       #         'demographics.views.email_and_fax_list' ,
                       #         name = 'email_and_fax_list'
                       #    ),

                       url(r'email_and_fax/add/(?P<id>\d+)/$',
                           'demographics.views.email_and_fax_add',
                           name='email_and_fax_add'
                           ),
                       url(r'email_and_fax/edit/(?P<id>\d+)/$',
                           'demographics.views.email_and_fax_edit',
                           name='email_and_fax_edit'
                           ),
                       url(r'email_and_fax/del/(?P<id>\d+)/$'		,
                           'demographics.views.email_and_fax_del'	,
                           name='email_and_fax_del'
                           ),


                       url(r'guardian/json/$',
                           'demographics.views.guardian_json',
                           name='guardian_json'
                           ),

                       #   url(r'guardian/list/(?P<id>\d+)/$', 
                             #'demographics.views.guardian_list',
                             #name = 'guardian_list' ),

                       url(r'guardian/add/(?P<id>\d+)/$',
                           'demographics.views.guardian_add',
                           name='guardian_add'
                           ),
                       url(r'guardian/edit/(?P<id>\d+)/$',
                           'demographics.views.guardian_edit',
                           name='guardian_edit'
                           ),
                       url(r'guardian/del/(?P<id>\d+)/$',
                           'demographics.views.guardian_del',
                           name='guardian_del'
                           ),


                       url(r'demographics/json/$',
                           'demographics.views.demographics_json',
                           name='demographics_json'
                           ),

                       #    url(r'demographics/list/(?P<id>\d+)/$',
                       #    	 'demographics.views.demographics_list',
                       #    	 name = 'demographics_list'
                       #    ),

                       url(r'demographics/add/(?P<id>\d+)/$',
                           'demographics.views.demographics_add',
                           name='demographics_add'
                           ),
                       url(r'demographics/edit/(?P<id>\d+)/$',
                           'demographics.views.demographics_edit',
                           name='demographics_edit'
                           ),
                       url(r'demographics/del/(?P<id>\d+)/$',
                           'demographics.views.demographics_del',
                           name='demographics_del'
                           ),
)
