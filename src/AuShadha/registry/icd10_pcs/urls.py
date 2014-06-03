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

from .dijit_widgets.pane import render_icd10_pcs_pane, \
                                get_icd10_pcs_pane,    \
                                render_icd10_pcs_related_items

from .dijit_widgets.tree import render_icd10_pcs_tree,                 \
                                render_all_section_tree,               \
                                render_per_section_body_system_tree,   \
                                render_per_body_system_operation_tree, \
                                render_per_operation_pcs_row

urlpatterns = patterns('',

                        url(r'get/pcstables/all/', get_all_pcstables_json, name = 'get_all_pcstables_json'),
                        url(r'get/pcsrows/all/', get_all_pcsrows_json, name = 'get_all_pcsrows_json'),
                        url(r'get/pcsrows/for/pcstable/(?P<pcstable_id>\d+)/$', get_pcsrows_for_pcstable, name = 'get_pcsrows_for_pcstable'),
                        url(r'get/bodyparts/for/pcsrow/(?P<pcsrow_id>\d+)/$', get_bodyparts_for_pcsrow, name = 'get_bodyparts_for_pcsrow'),
                        url(r'get/bodyparts/for/all_pcsrows/$', get_bodyparts_for_pcsrow, name = 'get_bodyparts_for_all_pcsrows'),
                        url(r'get/approaches/for/pcsrow/(?P<pcsrow_id>\d+)/$', get_approaches_for_pcsrow, name = 'get_approaches_for_pcsrow'),
                        url(r'get/devices/for/pcsrow/(?P<pcsrow_id>\d+)/$', get_devices_for_pcsrow, name = 'get_devices_for_pcsrow'),
  	                url(r'get/qualifiers/for/pcsrow/(?P<pcsrow_id>\d+)/$', get_qualifiers_for_pcsrow, name = 'get_qualifiers_for_pcsrow'),
                        url(r'get/(?P<node_name>\w+)/(?P<parent_node_id>\d+)/pane/$', get_icd10_pcs_pane, name = 'get_icd10_pcs_pane'),

                        url(r'code/search/$', icd10_pcs_code_search, name = 'icd10_pcs_code_search'),

                        url(r'render/pane/$', render_icd10_pcs_pane, name = 'render_icd10_pcs_pane'),
                        url(r'render/tree/$', render_icd10_pcs_tree, name = 'render_icd10_pcs_tree'),
                        url(r'render/all/section/tree/$', render_all_section_tree, name = 'render_all_section_tree'),
                        url(r'render/per/section/body_system/tree/(?P<section>\w+)/$', render_per_section_body_system_tree, name = 'render_per_section_body_system_tree'),
                        url(r'render/per/body_system/operation/tree/(?P<body_system>\w+)/$', render_per_body_system_operation_tree, name = 'render_per_body_system_operation_tree'),
                        url(r'render/per/operation/pcs_row/(?P<operation>\w+)/$', render_per_operation_pcs_row, name = 'render_per_operation_pcs_row'),
                        url(r'render/related_items/(?P<node_id>\d+)/$', render_icd10_pcs_related_items, name = 'render_icd10_pcs_related_items'),
                        url(r'render/(?P<node_name>\w+)/(?P<parent_node_id>\d+)/tree/$', render_icd10_pcs_tree, name = 'render_icd10_pcs_tree'),
                        url(r'render/related/(?P<node_name>)\w+/(?P<node_id>\d+)/$', render_icd10_pcs_related_items, name = 'icd10_pcs_render_related'),

)


