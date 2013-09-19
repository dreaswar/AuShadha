from django.conf.urls.defaults import *
from django.contrib import admin

import AuShadha.settings
from admission.views import *

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'json/$',
                           'admission.views.admission_json',
                           name='admission_json'
                           ),

                       #   url(r'list/(?P<id>\d+)/$',
                       #'admission.views.patient_admission_list',
                       #name = 'get_patient_admission_list'
                       #),

                       url(r'add/(?P<id>\d+)/$'	,
                           'admission.views.patient_admission_add',
                           name='patient_admission_add'
                           ),

                       url(r'add/$',
                           'admission.views.patient_admission_add',
                           name='patient_admission_add'
                           ),

                       )
