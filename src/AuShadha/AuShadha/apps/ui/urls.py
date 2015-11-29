from django.conf.urls import patterns, url
#from django.views.generic.simple import direct_to_template

import AuShadha.settings

from .views import home, get_reference_apps, installed_apps
from dijit_widgets.pane import render_aushadha_ui_pane
#from data.views import installed_apps

urlpatterns = patterns('',

                       url(r'home/$', home, name='home'),
                       url(r'json/installed_apps/$',
                           installed_apps, name='installed_apps'),
                       url(r'render/pane/$', render_aushadha_ui_pane,
                           name='render_aushadha_ui_pane'),
                       url(r'^$', home, name='home'),
                       url(r'get/reference_apps/$', get_reference_apps,
                           name='get_reference_apps'),

                       #(r'^AuShadha/json_data/', include('json_data.urls') ),
                       #(r'^AuShadha/widgets/', include('widgets.urls') ),
                       )
