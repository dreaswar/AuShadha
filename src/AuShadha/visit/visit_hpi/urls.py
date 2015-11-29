from django.conf.urls import *
#from django.contrib import admin
# admin.autodiscover()

import AuShadha.settings

from .views import *
#from .dijit_widgets.pane import render_visit_hpi_tree, render_visit_hpi_pane
from .utilities import get_all_visit_hpi, import_active_visit_hpi


urlpatterns = patterns('',

                       ########################################################

                       url(r'add/$',
                           visit_hpi_add,
                           name="visit_hpi_add_without_id"
                           ),

                       url(r'add/(?P<visit_id>\d+)/$',
                           visit_hpi_add,
                           name="visit_hpi_add"
                           ),

                       url(r'json/$',
                           visit_hpi_json,
                           name="visit_hpi_json_without_id"
                           ),

                       url(r'json/(?P<visit_id>\d+)/$',
                           visit_hpi_json,
                           name="visit_hpi_json"
                           ),

                       # url(r'list/(?P<visit_id>\d+)/$' ,
                       #visit_hpi_list ,
                       # name="visit_hpi_list"
                       #),

                       url(r'hpi/edit/$',
                           visit_hpi_edit,
                           name="visit_hpi_edit_without_id"
                           ),

                       url(r'hpi/edit/(?P<visit_hpi_id>\d+)/$',
                           visit_hpi_edit,
                           name="visit_hpi_edit"
                           ),

                       url(r'hpi/del/$',
                           visit_hpi_del,
                           name="visit_hpi_del_without_id"
                           ),

                       url(r'hpi/del/(?P<visit_hpi_id>\d+)/$',
                           visit_hpi_del,
                           name="visit_hpi_del"
                           ),

                       url(r'hpi/get_all_visit_hpi/(?P<visit_id>\d+)/$',
                           get_all_visit_hpi,
                           name="get_all_visit_hpi"
                           ),

                       # url(r'hpi/import_active_visit_hpi/(?P<visit_id>\d+)/$',
                       # import_active_visit_hpi,
                       # name="import_active_visit_hpi"
                       #),

                       ########################################################

                       )
