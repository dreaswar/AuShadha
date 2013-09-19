from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

import AuShadha.settings

from allergy_list.views import *

urlpatterns = patterns('',

                       url(r'json/$',
                           'allergy_list.views.allergy_json',
                           name='allergy_json'
                           ),

                       #    url(r'list/(?P<id>\d+)/$',
                       #    		'allergy_list.views.allergy_list',
                       #    		name = 'allergy_list'
                       #    ),

                       url(r'add/(?P<id>\d+)/$',
                           'allergy_list.views.allergy_add',
                           name='allergy_add'
                           ),
                       url(r'edit/(?P<id>\d+)/$',
                           'allergy_list.views.allergy_edit',
                           name='allergy_edit'
                           ),
                       url(r'del/(?P<id>\d+)/$',
                           'allergy_list.views.allergy_del',
                           name='allergy_del'
                           ),

)
