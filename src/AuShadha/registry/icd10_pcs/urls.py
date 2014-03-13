from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings
admin.autodiscover()

from .views import get_all_pcstables_json,    \
                   get_all_pcsrows_json,      \
                   get_all_devices_json,      \
                   get_all_qualifiers_json,   \
                   get_all_bodyparts_json,    \
                   get_all_approaches_json ,  \
                   get_pcsrows_for_pcstable,  \
                   get_bodyparts_for_pcsrow,  \
                   get_approaches_for_pcsrow, \
                   get_devices_for_pcsrow,    \
                   get_qualifiers_for_pcsrow, \
                   compose_icd10_pcs_code ,   \
                   get_all_icd10_pcs_codes,   \
                   icd10_pcs_code_search

from .dijit_widgets.pane import render_icd10_pcs_pane, get_icd10_pcs_pane, render_icd10_pcs_related_items
from .dijit_widgets.tree import render_icd10_pcs_tree

urlpatterns = patterns('',

                        url(r'get/pcstables/all/', get_all_pcstables_json, name = 'get_all_pcstables_json'),
                        url(r'get/pcsrows/all/', get_all_pcsrows_json, name = 'get_all_pcsrows_json'),
                        url(r'get/devices/all/', get_all_devices_json, name = 'get_all_devices_json'),
                        url(r'get/qualifiers/all/', get_all_qualifiers_json, name = 'get_all_qualifiers_json'),
                        url(r'get/bodyparts/all/', get_all_bodyparts_json, name = 'get_all_bodyparts_json'),
                        url(r'get/approaches/all/', get_all_approaches_json, name = 'get_all_approaches_json'),

                        url(r'get/pcsrows/for/pcstable/(?P<pcstable_id>\d+)/$', get_pcsrows_for_pcstable, name = 'get_pcsrows_for_pcstable'),
                        url(r'get/bodyparts/for/pcsrow/(?P<pcsrow_id>\d+)/$', get_bodyparts_for_pcsrow, name = 'get_bodyparts_for_pcsrow'),
                        url(r'get/approaches/for/pcsrow/(?P<pcsrow_id>\d+)/$', get_approaches_for_pcsrow, name = 'get_approaches_for_pcsrow'),
                        url(r'get/devices/for/pcsrow/(?P<pcsrow_id>\d+)/$', get_devices_for_pcsrow, name = 'get_devices_for_pcsrow'),
  	                url(r'get/qualifiers/for/pcsrow/(?P<pcsrow_id>\d+)/$', get_qualifiers_for_pcsrow, name = 'get_qualifiers_for_pcsrow'),

                        url(r'compose/code/(?P<pcstable_id>\d+)/(?P<pcsrow_id>\d+)/(?P<bodypart_id>\d+)/(?P<approach_id>\d+)/(?P<device_id>\d+)/(?P<qualifier_id>\d+)/$ ',
                            compose_icd10_pcs_code,
                            name = 'compose_icd10_pcs_code'
                        ),
                        
                        url(r'get/all/codes/$', get_all_icd10_pcs_codes,name = 'get_all_icd10_pcs_codes'),
                        url(r'code/search/$', icd10_pcs_code_search, name = 'icd10_pcs_code_search'),

#                        url(r'get/pcstables/tree/$', icd10_pcstables_tree, name  = 'icd10_pcstables_tree'),
#                        url(r'get/pcsrows/tree/$', icd10_pcsrows_tree, name = 'icd10_pcsrows_tree'),
#                        url(r'get/bodyparts/tree/$', icd10_bodyparts_tree, name= 'icd10_bodyparts_tree'),
#                        url(r'get/approaches/tree/$', icd10_approaches_tree, name = 'icd10_approaches_tree'),
#                        url(r'get/devices/tree/$', icd10_devices_tree, name  = 'icd10_devices_tree'),
#                        url(r'get/qualifiers/tree/$', icd10_qualifiers_tree, name = 'icd10_qualifiers_tree'),

                        url(r'render/pane/$', render_icd10_pcs_pane, name = 'render_icd10_pcs_pane'),
                        url(r'get/(?P<node_name>\w+)/(?P<parent_node_id>\d+)/pane/$', get_icd10_pcs_pane, name = 'get_icd10_pcs_pane'),
                        url(r'render/tree/$', render_icd10_pcs_tree, name = 'render_icd10_pcs_tree'),
                        url(r'render/(?P<node_name>\w+)/(?P<parent_node_id>\d+)/tree/$', render_icd10_pcs_tree, name = 'render_icd10_pcs_tree'),
                        url(r'render/related_items/(?P<node_id>\d+)/$', render_icd10_pcs_related_items, name = 'render_icd10_pcs_related_items'),

)


