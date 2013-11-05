from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings
admin.autodiscover()

from .views import email_and_fax_json,email_and_fax_add,email_and_fax_edit,email_and_fax_del

urlpatterns = patterns('',

                       url(r'json/$',
                           email_and_fax_json,
                           name='email_and_fax_json'
                           ),

                       url(r'json/(?P<patient_id>\d+)/$',
                           email_and_fax_json,
                           name='email_and_fax_json_with_id'
                           ),

                       #    url(r'list/(?P<id>\d+)/$',
                       #        email_and_fax_list,
                       #        name = 'patient_email_and_fax_list'
                       #    ),

                        url(r'add/$',
                           email_and_fax_add,
                           name='email_and_fax_add_without_id'
                           ),
                       
                       url(r'add/(?P<patient_id>\d+)/$',
                           email_and_fax_add,
                           name='email_and_fax_add_with_id'
                           ),

                       url(r'edit/$',
                           email_and_fax_edit,
                           name='email_and_fax_edit_without_id'
                           ),
                       url(r'edit/(?P<email_and_fax_id>\d+)/$',
                           email_and_fax_edit,
                           name='email_and_fax_edit_with_id'
                           ),

                       url(r'del/$',
                           email_and_fax_del,
                           name='email_and_fax_del_without_id'
                           ),

                       url(r'del/(?P<email_and_fax_id>\d+)/$',
                           email_and_fax_del,
                           name='email_and_fax_del_with_id'
                           )
)
