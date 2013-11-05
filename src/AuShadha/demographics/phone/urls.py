from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings
admin.autodiscover()

from .views import phone_json,phone_add,phone_edit,phone_del

urlpatterns = patterns('',

                       url(r'json/$',
                           phone_json,
                           name='phone_json'
                           ),

                       url(r'json/(?P<patient_id>\d+)/$',
                           phone_json,
                           name='phone_json_with_id'
                           ),

                       #    url(r'list/(?P<id>\d+)/$',
                       #        phone_list,
                       #        name = 'patient_phone_list'
                       #    ),

                        url(r'add/$',
                           phone_add,
                           name='phone_add_without_id'
                           ),
                       
                       url(r'add/(?P<patient_id>\d+)/$',
                           phone_add,
                           name='phone_add_with_id'
                           ),

                       url(r'edit/$',
                           phone_edit,
                           name='phone_edit_without_id'
                           ),
                       url(r'edit/(?P<phone_id>\d+)/$',
                           phone_edit,
                           name='phone_edit_with_id'
                           ),

                       url(r'del/$',
                           phone_del,
                           name='phone_del_without_id'
                           ),

                       url(r'del/(?P<phone_id>\d+)/$',
                           phone_del,
                           name='phone_del_with_id'
                           )
)
