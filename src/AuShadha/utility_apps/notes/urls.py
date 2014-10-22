from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from notes.views import *
from notes.dijit_widgets.pane import render_notes_pane
from notes.dijit_widgets.tree import render_notes_tree

admin.autodiscover()

urlpatterns = patterns('',

################################ CRUD ##################################
                       url(r'notes/list/(?P<id>\d+)/$',
                           'notes.views.notes_detail_list',
                           name='notes_detail_list'
                           ),

                       url(r'notes/add/(?P<id>\d+)/$',
                           'notes.views.notes_detail_add',
                           name='notes_detail_add'
                           ),

                       url(r'notes/edit/(?P<id>\d+)/$',
                           'notes.views.notes_detail_edit',
                           name='notes_detail_edit'
                           ),

                       url(r'notes/del/(?P<id>\d+)/$',
                           'notes.views.notes_detail_del',
                           name='notes_detail_del'
                           ),

################################ JSON, UI-PANE & TREE #########################

                      url(r'notes/pane/(?P<id>\d+)/$',
                           'notes.dijit_widgets.pane.render_notes_pane',
                           name='render_notes_pane_with_id'
                           ),

                      url(r'notes/pane/$',
                           'notes.dijit_widgets.pane.render_notes_pane',
                           name='render_notes_pane_without_id'
                           ),

                       url(r'notes/tree/(?P<id>\d+)/$',
                           'notes.views.render_notes_tree',
                           name='render_notes_tree_with_id'
                           ),

                       url(r'notes/tree/$',
                           'notes.views.render_notes_tree',
                           name='render_notes_tree_without_id'
                           ),

                       url(r'notes/json/$',
                           'notes.views.render_notes_json',
                           name='render_notes_json_without_id'
                           ),

                       url(r'notes/json/(?P<id>\d+)/$',
                           'notes.views.render_notes_json',
                           name='render_notes_json_with_id'
                           ),

################################ SUMMARY ###############################

                       url(r'notes/summary/$',
                           'notes.views.render_notes_summary',
                           name='render_notes_summary_without_id'
                           ),

                       url(r'notes/summary/(?P<id>\d+)/$',
                           'notes.views.render_notes_summary',
                           name='render_notes_summary_with_id'
                           ),

)
