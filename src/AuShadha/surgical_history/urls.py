from django.conf.urls.defaults import *
from django.contrib import admin

import AuShadha.settings
from surgical_history.views import *

admin.autodiscover()

urlpatterns = patterns('',

                url(r'json/$',
                    'surgical_history.views.surgical_history_json',
                    name='surgical_history_json'
                    ),

                # url(r'list/(?P<id>\d+)/$',
                #'surgical_history.views.surgical_history_list',
                #name = 'surgical_history_list'
                #),

                url(r'add/(?P<id>\d+)/$',
                    'surgical_history.views.surgical_history_add',
                    name='surgical_history_add'
                    ),

                url(r'edit/(?P<id>\d+)/$',
                    'surgical_history.views.surgical_history_edit',
                    name='surgical_history_edit'
                    ),
                url(r'del/(?P<id>\d+)/$',
                    'surgical_history.views.surgical_history_del',
                    name='surgical_history_del'
                    )
)
