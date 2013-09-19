from django.conf.urls.defaults import *
from django.contrib import admin

import AuShadha.settings
from family_history.views import *

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'json/$',
                           'family_history.views.family_history_json',
                           name='family_history_json'
                           ),

                       #    url(r'list/(?P<id>\d+)/$',
                       #    		'family_history.views.family_history_list',
                       #    		name = 'family_history_list'
                       #    ),

                       url(r'add/(?P<id>\d+)/$',
                           'family_history.views.family_history_add',
                           name='family_history_add'
                           ),
                       url(r'edit/(?P<id>\d+)/$',
                           'family_history.views.family_history_edit',
                           name='family_history_edit'
                           ),
                       url(r'del/(?P<id>\d+)/$',
                           'family_history.views.family_history_del',
                           name='family_history_del'
                           ),
)
