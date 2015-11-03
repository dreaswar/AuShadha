from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from simplenotes.views import *
#from simplenotes.dijit_widgets.pane import render_pane
#from simplenotes.dijit_widgets.tree import render_tree

admin.autodiscover()

urlpatterns = patterns('',

################################ PATIENT CRUD ##################################

                       url(r'add/(?P<visit_detail_id>\d+)/$'                             ,
                           'simplenotes.views.simplenotes_firstvisit_add',
                           name='simplenotes_firstvisit_add'
                           ),

                       url(r'simplenotes/edit/(?P<simplenotes_id>\d+)/$',
                           'simplenotes.views.simplnotes_edit',
                           name='simplenotes_edit'
                           ),
                       url(r'simplenotes/del/(?P<simplenotes_id>\d+)/$',
                           'simplenotes.views.simplenotes_del',
                           name='simplenotes_del'
                           ),


################################  JSON ##################################

                       url(r'simplenotes/json/$',
                           'simplenotes.views.render_simplenotes_json',
                           name='render_simplenotes_json'
                           ),


################################  SUMMARY ###############################

                       url(r'simplenotes/summary/$',
                           'simplenotes.views.render_summary',
                           name='render_simplenotes_summary_without_id'
                           ),

                       url(r'simplenotes/summary/(?P<patient_id>\d+)/$',
                           'simplenotes.views.render_summary',
                           name='render_simplenotes_summary_with_id'
                           ),


################################  PANE ##################################

                      url(r'simplenotes/pane/(?P<visit_detail_id>\d+)/$',
                           'simplenotes.dijit_widgets.pane.render_pane',
                           name='render_simplenotes_pane_with_id'
                           ),

                      url(r'simplenotes/pane/$',
                           'simplenotes.dijit_widgets.pane.render_pane',
                           name='render_simplenotes_pane_without_id'
                           ),

################################  TREE ##################################

                       url(r'simplenotes/tree/(?P<visit_detail_id>\d+)/$',
                           'simplenotes.dijit_widgets.tree.render_tree',
                           name='render_simplenotes_tree_with_id'
                           ),

                       url(r'simplenotes/tree/$',
                           'simplenotes.dijit_widgets.tree.render_tree',
                           name='render_simplenotes_tree_without_id'
                           ),

)
