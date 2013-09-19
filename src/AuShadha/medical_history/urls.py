from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings

from medical_history.views import *

admin.autodiscover()

urlpatterns = patterns('',

                  url(r'json/$',
                      'medical_history.views.medical_history_json',
                      name='medical_history_json'
                      ),

                  # url(r'list/(?P<id>\d+)/$',
                  #'medical_history.views.medical_history_list',
                  #name = 'medical_history_list'
                  #),

                  url(r'add/(?P<id>\d+)/$',
                      'medical_history.views.medical_history_add',
                      name='medical_history_add'
                      ),

                  url(r'edit/(?P<id>\d+)/$',
                      'medical_history.views.medical_history_edit',
                      name='medical_history_edit'
                      ),
                  url(r'del/(?P<id>\d+)/$',
                      'medical_history.views.medical_history_del',
                      name='medical_history_del'
                      ),
)
