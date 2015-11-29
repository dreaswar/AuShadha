from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from messenger.views import *
from messenger.dijit_widgets.pane import render_messenger_pane
from messenger.dijit_widgets.tree import render_messenger_tree

admin.autodiscover()

urlpatterns = patterns('',

                       ################################ CRUD ##################
                       url(r'messenger/list/(?P<id>\d+)/$',
                           'messenger.views.messenger_detail_list',
                           name='messenger_detail_list'
                           ),

                       url(r'messenger/add/(?P<id>\d+)/$',
                           'messenger.views.messenger_detail_add',
                           name='messenger_detail_add'
                           ),

                       url(r'messenger/edit/(?P<id>\d+)/$',
                           'messenger.views.messenger_detail_edit',
                           name='messenger_detail_edit'
                           ),

                       url(r'messenger/del/(?P<id>\d+)/$',
                           'messenger.views.messenger_detail_del',
                           name='messenger_detail_del'
                           ),

                       ################################ JSON, UI-PANE & TREE ##

                       url(r'messenger/pane/(?P<id>\d+)/$',
                           'messenger.dijit_widgets.pane.render_messenger_pane',
                           name='render_messenger_pane_with_id'
                           ),

                       url(r'messenger/pane/$',
                           'messenger.dijit_widgets.pane.render_messenger_pane',
                           name='render_messenger_pane_without_id'
                           ),

                       url(r'messenger/tree/(?P<id>\d+)/$',
                           'messenger.views.render_messenger_tree',
                           name='render_messenger_tree_with_id'
                           ),

                       url(r'messenger/tree/$',
                           'messenger.views.render_messenger_tree',
                           name='render_messenger_tree_without_id'
                           ),

                       url(r'messenger/json/$',
                           'messenger.views.render_messenger_json',
                           name='render_messenger_json_without_id'
                           ),

                       url(r'messenger/json/(?P<id>\d+)/$',
                           'messenger.views.render_messenger_json',
                           name='render_messenger_json_with_id'
                           ),

                       ################################ SUMMARY ###############

                       url(r'messenger/summary/$',
                           'messenger.views.render_messenger_summary',
                           name='render_messenger_summary_without_id'
                           ),

                       url(r'messenger/summary/(?P<id>\d+)/$',
                           'messenger.views.render_messenger_summary',
                           name='render_messenger_summary_with_id'
                           ),

                       )
