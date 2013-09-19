from django.conf.urls.defaults import *
from django.contrib import admin

import AuShadha.settings
from medication_list.views import *

admin.autodiscover()

urlpatterns = patterns('',


                       url(r'json/$',
                           'medication_list.views.medication_list_json',
                           name='medication_list_json'
                           ),

                       #    url(r'list/(?P<id>\d+)/$',
                       #    		'medication_list.views.medication_list_list',
                       #    		name = 'medication_list_list'
                       #    ),

                       url(r'add/(?P<id>\d+)/$',
                           'medication_list.views.medication_list_add',
                           name='medication_list_add'
                           ),
                       url(r'edit/(?P<id>\d+)/$',
                           'medication_list.views.medication_list_edit',
                           name='medication_list_edit'
                           ),
                       url(r'del/(?P<id>\d+)/$',
                           'medication_list.views.medication_list_del',
                           name='medication_list_del'
                           ),
)
