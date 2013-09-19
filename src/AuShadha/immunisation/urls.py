from django.conf.urls.defaults import *
from django.contrib import admin

import AuShadha.settings
from immunisation.views import *

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'json/$',
                           'immunisation.views.immunisation_json',
                           name='immunisation_json'
                           ),

                       #    url(r'list/(?P<id>\d+)/$',
                    #    		'immunisation.views.immunisation_list',
                    #    		name = 'immunisation_list'
                       #    ),

                       url(r'add/(?P<id>\d+)/$',
                           'immunisation.views.immunisation_add',
                           name='immunisation_add'
                           ),
                       url(r'edit/(?P<id>\d+)/$',
                           'immunisation.views.immunisation_edit',
                           name='immunisation_edit'
                           ),
                       url(r'del/(?P<id>\d+)/$',
                           'immunisation.views.immunisation_del',
                           name='immunisation_del'
                           ),
)
