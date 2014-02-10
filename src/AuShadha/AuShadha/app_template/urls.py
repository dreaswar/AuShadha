from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings

from {{app_name}}.views import *
from {{app_name}}.dijit_widgets.pane import render_{{app_name}}_pane
from {{app_name}}.dijit_widgets.tree import render_{{app_name}}_tree

admin.autodiscover()

urlpatterns = patterns('',

################################ CRUD ##################################
                       url(r'{{app_name}}/list/(?P<id>\d+)/$',
                           '{{app_name}}.views.{{app_name}}_detail_list',
                           name='{{app_name}}_detail_list'
                           ),

                       url(r'{{app_name}}/add/(?P<id>\d+)/$',
                           '{{app_name}}.views.{{app_name}}_detail_add',
                           name='{{app_name}}_detail_add'
                           ),

                       url(r'{{app_name}}/edit/(?P<id>\d+)/$',
                           '{{app_name}}.views.{{app_name}}_detail_edit',
                           name='{{app_name}}_detail_edit'
                           ),

                       url(r'{{app_name}}/del/(?P<id>\d+)/$',
                           '{{app_name}}.views.{{app_name}}_detail_del',
                           name='{{app_name}}_detail_del'
                           ),

################################ JSON, UI-PANE & TREE #########################

                      url(r'{{app_name}}/pane/(?P<id>\d+)/$',
                           '{{app_name}}.dijit_widgets.pane.render_{{app_name}}_pane',
                           name='render_{{app_name}}_pane_with_id'
                           ),

                      url(r'{{app_name}}/pane/$',
                           '{{app_name}}.dijit_widgets.pane.render_{{app_name}}_pane',
                           name='render_{{app_name}}_pane_without_id'
                           ),

                       url(r'{{app_name}}/tree/(?P<id>\d+)/$',
                           '{{app_name}}.views.render_{{app_name}}_tree',
                           name='render_{{app_name}}_tree_with_id'
                           ),

                       url(r'{{app_name}}/tree/$',
                           '{{app_name}}.views.render_{{app_name}}_tree',
                           name='render_{{app_name}}_tree_without_id'
                           ),

                       url(r'{{app_name}}/json/$',
                           '{{app_name}}.views.render_{{app_name}}_json',
                           name='render_{{app_name}}_json_without_id'
                           ),

                       url(r'{{app_name}}/json/(?P<id>\d+)/$',
                           '{{app_name}}.views.render_{{app_name}}_json',
                           name='render_{{app_name}}_json_with_id'
                           ),

################################ SUMMARY ###############################

                       url(r'{{app_name}}/summary/$',
                           '{{app_name}}.views.render_{{app_name}}_summary',
                           name='render_{{app_name}}_summary_without_id'
                           ),

                       url(r'{{app_name}}/summary/(?P<id>\d+)/$',
                           '{{app_name}}.views.render_{{app_name}}_summary',
                           name='render_{{app_name}}_summary_with_id'
                           ),

)
