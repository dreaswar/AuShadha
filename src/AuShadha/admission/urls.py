
from django.conf.urls.defaults import *
#from django.contrib import admin
from django.conf.urls.defaults import patterns, url

import AuShadha.settings
from admission.views import *

#admin.autodiscover()

urlpatterns = patterns('',

                       url(r'json/$',
                           'admission.views.admission_json',
                           name='admission_json'
                           ),

                       #   url(r'list/(?P<id>\d+)/$',
                       #'admission.views.admission_list',
                       #name = 'get_admission_list'
                       #),

                       url(r'add/(?P<id>\d+)/$'	,
                           'admission.views.admission_add',
                           name='admission_add'
                           ),

                       url(r'add/$',
                           'admission.views.admission_add',
                           name='admission_add'
                           ),

################################ ADMISSION TREE ##################################

                       url(r'admission/tree/(?P<admission_id>\d+)/$',
                           'admission.views.render_admission_tree',
                           name='render_admission_tree_with_id'
                           ),

                       url(r'admission/tree/$',
                           'admission.views.render_admission_tree',
                           name='render_admission_tree_without_id'
                           )
)
