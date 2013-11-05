from django.conf.urls.defaults import patterns, url
#from django.views.generic.simple import direct_to_template

import AuShadha.settings

from .views import home
from data.views import installed_apps

urlpatterns = patterns('',

                      url(r'home/$',  home, name='home'),
                      url(r'json/installed_apps/$',  installed_apps, name='installed_apps'),

                      #(r'^AuShadha/json_data/', include('json_data.urls') ),
                      #(r'^AuShadha/widgets/', include('widgets.urls') ),
) 
