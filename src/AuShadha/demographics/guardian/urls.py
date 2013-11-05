from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings
admin.autodiscover()

from .views import guardian_json,guardian_add,guardian_edit,guardian_del

urlpatterns = patterns('',

                       url(r'json/$',
                           guardian_json,
                           name='guardian_json'
                           ),

                       url(r'json/(?P<patient_id>\d+)/$',
                           guardian_json,
                           name='guardian_json_with_id'
                           ),

                       #    url(r'list/(?P<id>\d+)/$',
                       #        guardian_list,
                       #        name = 'patient_guardian_list'
                       #    ),

                        url(r'add/$',
                           guardian_add,
                           name='guardian_add_without_id'
                           ),
                       
                       url(r'add/(?P<patient_id>\d+)/$',
                           guardian_add,
                           name='guardian_add_with_id'
                           ),

                       url(r'edit/$',
                           guardian_edit,
                           name='guardian_edit_without_id'
                           ),
                       url(r'edit/(?P<guardian_id>\d+)/$',
                           guardian_edit,
                           name='guardian_edit_with_id'
                           ),

                       url(r'del/$',
                           guardian_del,
                           name='guardian_del_without_id'
                           ),

                       url(r'del/(?P<guardian_id>\d+)/$',
                           guardian_del,
                           name='guardian_del_with_id'
                           )
)
