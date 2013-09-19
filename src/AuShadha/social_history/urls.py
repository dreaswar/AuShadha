from django.conf.urls.defaults import *
from django.contrib import admin

import AuShadha.settings
from social_history.views import *

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'json/$',
                           'social_history.views.social_history_json',
                           name='social_history_json'
                           ),

                       #    url(r'list/(?P<id>\d+)/$',
                       #    	 'social_history.views.social_history_list',
                       #    	 name = 'social_history_list'
                       #    ),

                       url(r'add/(?P<id>\d+)/$',
                           'social_history.views.social_history_add',
                           name='social_history_add'
                           ),
                       url(r'edit/(?P<id>\d+)/$',
                           'social_history.views.social_history_edit',
                           name='social_history_edit'
                           ),
                       url(r'del/(?P<id>\d+)/$',
                           'social_history.views.social_history_del',
                           name='social_history_del'
                           ),
)
