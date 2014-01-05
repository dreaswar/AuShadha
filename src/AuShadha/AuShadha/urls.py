from django.conf.urls.defaults import patterns, url, include
#from django.views.generic.simple import direct_to_template

import settings
#from AuShadha.apps.ui import autodiscover as autodiscover_ui
#from AuShadha.apps.ui.ui import ui as UI
from django.contrib import admin

admin.autodiscover()

#print "Trying to autodiscover UI for AuShadha"
#autodiscover_ui()
#print "Finished autodiscovering"

urlpatterns = patterns('',

                       # Specific URLS..
                       #(r'^AuShadha/clinic/',include('AuShadha.apps.clinic.urls')),

                      url(r'^AuShadha/search/', include('AuShadha.apps.search.urls') ),

                      url(r'^AuShadha/ui/', include('AuShadha.apps.ui.urls') ),

                      url(r'^AuShadha/pat/', include('patient.urls') ),
                      url(r'^AuShadha/patient/', include('patient.urls') ),
                      url(r'^AuShadha/patient/', include('patient.urls') ),

                      url(r'^AuShadha/admission/', include('admission.admission.urls') ),

                      url(r'^AuShadha/demographics/', include('demographics.demographics.urls') ),
                      url(r'^AuShadha/contact/', include('demographics.contact.urls') ),
                      url(r'^AuShadha/phone/', include('demographics.phone.urls') ),
                      url(r'^AuShadha/guardian/', include('demographics.guardian.urls') ),

                      #url(r'^AuShadha/email_and_fax/', include('demographics.email_and_fax.urls') ),                      

                      url(r'^AuShadha/family_history/', include('history.family_history.urls')),
                      url(r'^AuShadha/social_history/', include('history.social_history.urls')),
                      url(r'^AuShadha/medical_history/', include('history.medical_history.urls')),
                      url(r'^AuShadha/surgical_history/', include('history.surgical_history.urls')),

                      #url(r'^AuShadha/obs_and_gyn/', include('history.obs_and_gyn.urls') ),                      

                      url(r'^AuShadha/medication_list/', include('medication_list.urls') ),
                      url(r'^AuShadha/allergy_list/', include('allergy_list.urls') ),
                      url(r'^AuShadha/immunisation/', include('immunisation.urls') ),


                      url(r'^AuShadha/visit/'             , include('visit.visit.urls')),
                      url(r'^AuShadha/visit_complaint/'   , include('visit.visit_complaints.urls') ),
                      url(r'^AuShadha/visit_complaints/'  , include('visit.visit_complaints.urls') ),
                      url(r'^AuShadha/visit_hpi/'         , include('visit.visit_hpi.urls') ),
                      url(r'^AuShadha/visit_ros/'         , include('visit.visit_ros.urls') ),
                      url(r'^AuShadha/visit_phyexam/'                     , include('visit.visit_phyexam.urls') ),
                      url(r'^AuShadha/visit_assessment_and_plan/'         , include('visit.visit_assessment_and_plan.urls') ),
                      url(r'^AuShadha/visit_soap/'                        , include('visit.visit_soap.urls') ),

#                      url(r'^AuShadha/follow_up/', include('visit.urls')),
#                      url(r'^AuShadha/phyexam/', include('phyexam.urls')),

                       # Admin and Admin Docs URL:
                      url(r'^AuShadha/admin/', include(admin.site.urls)),
                      url(r'^AuShadha/admin/doc/', include('django.contrib.admindocs.urls')),

                       # Media URL
                      url( r'^AuShadha/media/(?P<path>.*)$', 
                            'django.views.static.serve',
                            {'document_root': settings.MEDIA_ROOT}, 
                            'show_indexes:True'
                       ),

                       # Home URL
                       # TODO This will be the true address.. a kind of like a Dashboard. 
                       #      Till then use the one below for /AuShadha/home/
                       #(r'^AuShadha/home/$', 'home.views.home'),
                      #(r'^AuShadha/home/$', 'patient.views.patient_list'),

                       # Login and Logout URLS
                      (r'^AuShadha/$', include('AuShadha.apps.ui.urls')),
                      (r'^AuShadha/login/$','AuShadha.apps.aushadha_users.views.login_view'),
                      (r'^AuShadha/logout/$','AuShadha.apps.aushadha_users.views.logout_view'),

                       # If it dosent match anything else..
                      #(r'^AuShadha/alternate_layout/$','patient.views.alternate_layout'),
                      #(r'^AuShadha/$', 'patient.views.patient_list'),
                      #(r'^$', 'patient.views.patient_list'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views', url(
        r'^AuShadha/static/(?P<path>.*)$', 'serve'), )

