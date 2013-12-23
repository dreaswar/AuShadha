from django.conf.urls.defaults import *
#from django.contrib import admin
import AuShadha.settings

from .views import *
from .dijit_widgets.pane import render_visit_tree, render_visit_pane

#admin.autodiscover()

urlpatterns = patterns('',

################################################################################

                      url(r'json/(?P<patient_id>\d+)/$'  , 
                          visit_json  , 
                          name="render_visit_json"
                      ),

                      url(r'json/$', 
                          visit_json,
                          name='render_visit_json_without_id'
                      ),

                      url(r'pane/(?P<patient_id>\d+)/$', 
                          render_visit_pane,
                          name='render_visit_pane_with_id'
                      ),

                      url(r'pane/$', 
                          render_visit_pane,
                          name='render_visit_pane_without_id'
                      ),

                      url(r'render_visit_list/$', 
                          render_visit_list, 
                          name="render_visit_list"
                      ),

                      #url(r'tree/(?P<patient_id>\d+)/$',
                          #"visit.views.render_visit_tree", 
                          #name="render_visit_tree"
                      #),

                      #url(r'tree/$',
                          #"visit.views.render_visit_tree", 
                          #name="render_visit_tree_without_id"
                      #),

                      url(r'tree/(?P<patient_id>\d+)/$',
                          render_visit_tree, 
                          name="render_visit_tree"
                      ),

                      url(r'tree/$',
                          render_visit_tree, 
                          name="render_visit_tree_without_id"
                      ),

                       url(r'summary/(?P<patient_id>\d+)/$',
                          "visit.visit.views.visit_summary", 
                           name="visit_summary"
                           ),

                      url(r'summary/$',
                           "visit.visit.views.visit_summary", 
                           name="visit_summary_without_id"
                           ),

                      url(r'get/visit_detail/edit_pane_header/(?P<visit_id>\d+)/$',
                           'visit.visit.views.get_visit_detail_edit_pane_header', 
                           name="get_visit_detail_edit_pane_header"
                           ),

################################################################################

#                       url(r'render_patient_visits_pdf/(?P<patient_id>\d+)/$',
#                           'visit.views.render_patient_visits_pdf',
#                           name='render_patient_visits_pdf'
#                           ),

#                       url(r'render_visit_pdf/(?P<patient_id>\d+)/$',
#                           'visit.views.render_visit_pdf',
#                           name='render_visit_pdf'
#                           ),


################################################################################

                       url(r'detail/add/(?P<patient_id>\d+)/$',
                           visit_detail_add, 
                           name="visit_detail_add"
                           ),

                       url(r'detail/close/(?P<visit_id>\d+)/$',
                           visit_detail_close, 
                           name="visit_detail_close"
                           ),

                       url(r'detail/list/(?P<patient_id>\d+)/$',
                           visit_detail_list, 
                           name="visit_detail_list"),

                       url(r'detail/edit/(?P<visit_id>\d+)/$',
                           visit_detail_edit, 
                           name="visit_detail_edit"),

                       url(r'detail/del/(?P<visit_id>\d+)/$',
                           visit_detail_del, 
                           name="visit_detail_del"),

################################################################################

                       url(r'add/(?P<patient_id>\d+)/$',
                           visit_detail_add, 
                           name="visit_add"
                           ),

                       url(r'add/$',
                           visit_detail_add, 
                           name="visit_add_without_id"
                           ),

                       url(r'list/(?P<patient_id>\d+)/$',
                           visit_detail_list, 
                           name="visit_list"
                           ),

                       url(r'edit/(?P<visit_id>\d+)/$',
                           visit_detail_edit, 
                           name="visit_edit"
                           ),
                       url(r'edit/$',
                           visit_detail_edit, 
                           name="visit_edit_without_id"
                           ),

                       url(r'close/(?P<visit_id>\d+)/$'       , 
                           visit_detail_close       , 
                           name="visit_close"
                           ),

                       url(r'close/$'       , 
                           visit_detail_close       , 
                           name="visit_close_without_id"
                           ),

                       url(r'del/(?P<visit_id>\d+)/$',
                           visit_detail_del, 
                           name="visit_del"
                           ),
                       url(r'del/$',
                           visit_detail_del, 
                           name="visit_del_without_id"
                           ),

)
