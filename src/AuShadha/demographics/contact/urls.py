from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings
admin.autodiscover()

from .views import contact_json,contact_add,contact_edit,contact_del

urlpatterns = patterns('',

                       url(r'json/$',
                           contact_json,
                           name='contact_json'
                           ),

                       url(r'json/(?P<patient_id>\d+)/$',
                           contact_json,
                           name='contact_json_with_id'
                           ),

                       #    url(r'list/(?P<id>\d+)/$',
                       #   		contact_list,
                       #   		name = 'patient_contact_list'
                       #    ),

                        url(r'add/$',
                           contact_add,
                           name='contact_add_without_id'
                           ),
                       
                       url(r'add/(?P<patient_id>\d+)/$',
                           contact_add,
                           name='contact_add_with_id'
                           ),

                       url(r'edit/$',
                           contact_edit,
                           name='contact_edit_without_id'
                           ),
                       url(r'edit/(?P<contact_id>\d+)/$',
                           contact_edit,
                           name='contact_edit_with_id'
                           ),

                       url(r'del/$',
                           contact_del,
                           name='contact_del_without_id'
                           ),

                       url(r'del/(?P<contact_id>\d+)/$',
                           contact_del,
                           name='contact_del_with_id'
                           )
)
