from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

#Specific URLS..
#(r'^AuShadha/clinic/',         include('clinic.urls')),
(r'^AuShadha/pat/',            include('patient.urls')),
(r'^AuShadha/patient/',        include('patient.urls')),
#(r'^AuShadha/visit/',          include('visit.urls')),
#(r'^AuShadha/admission/',      include('admission.urls')),

#(r'^AuShadha/history/'       ,     include('history.urls')),
#(r'^AuShadha/phyexam/'       ,     include('phyexam.urls')),
#(r'^AuShadha/procedure/'     ,     include('procedure.urls')),
#(r'^AuShadha/discharge/'     ,     include('discharge.urls')),
#(r'^AuShadha/allergy/'       ,     include('allergydatabase.urls')),
#(r'^AuShadha/drugdatabase/'  ,     include('drugdatabase.urls')),
#(r'^AuShadha/calendar/'               ,     include('calendar.urls')),
#(r'^AuShadha/prescription/'            ,     include('prescription.urls')),



## Admin and Admin Docs URL:
(r'^AuShadha/admin/'     , include(admin.site.urls)),
(r'^AuShadha/admin/doc/' , include('django.contrib.admindocs.urls')),

## Media URL
(r'^AuShadha/media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT},'show_indexes:True'),

## Home URL
#TODO This will be the true address.. a kind of like a Dashboard. Till then use the one below for /AuShadha/home/
#(r'^AuShadha/home/$', 'home.views.home'),
(r'^AuShadha/home/$', 'patient.views.patient_list'),

## Login and Logout URLS
#(r'^AuShadha/login/$', 'django.contrib.auth.views.login'),
(r'^AuShadha/login/$', 'patient.views.login_view'),
(r'^AuShadha/logout/$', 'patient.views.logout_view'),

## If it dosent match anything else.. 
(r'^AuShadha/alternate_layout/$', 'patient.views.alternate_layout'),
(r'^AuShadha/$', 'patient.views.patient_list'),
(r'^$'         , 'patient.views.patient_list'),

)

if settings.DEBUG:
  urlpatterns += patterns('django.contrib.staticfiles.views',url(r'^AuShadha/static/(?P<path>.*)$', 'serve'), )
