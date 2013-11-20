from django.conf.urls.defaults import *
from django.contrib import admin
import AuShadha.settings
admin.autodiscover()

from .views import demographics_json,demographics_add,demographics_edit,demographics_del
from .dijit_widgets.pane import render_demographics_pane

urlpatterns = patterns('',

                       url(r'json/$',
                           demographics_json,
                           name='demographics_json'
                           ),

                       url(r'json/(?P<patient_id>\d+)/$',
                           demographics_json,
                           name='demographics_json_with_id'
                           ),

                       url(r'pane/(?P<patient_id>\d+)/$',
                           render_demographics_pane,
                           name='render_demographics_pane_with_id'
                           ),

                       url(r'pane/$',
                           render_demographics_pane,
                           name='render_demographics_pane_without_id'
                           ),

                       #    url(r'list/(?P<id>\d+)/$',
                       #        demographics_list,
                       #        name = 'patient_demographics_list'
                       #    ),

                        url(r'add/$',
                           demographics_add,
                           name='demographics_add_without_id'
                           ),
                       
                       url(r'add/(?P<patient_id>\d+)/$',
                           demographics_add,
                           name='demographics_add_with_id'
                           ),

                       url(r'edit/$',
                           demographics_edit,
                           name='demographics_edit_without_id'
                           ),
                       url(r'edit/(?P<demographics_id>\d+)/$',
                           demographics_edit,
                           name='demographics_edit_with_id'
                           ),

                       url(r'del/$',
                           demographics_del,
                           name='demographics_del_without_id'
                           ),

                       url(r'del/(?P<demographics_id>\d+)/$',
                           demographics_del,
                           name='demographics_del_with_id'
                           )
)
