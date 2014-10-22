from django.conf.urls import *
#from django.contrib import admin
#admin.autodiscover()

import AuShadha.settings

from .views import *
#from .dijit_widgets.pane import render_visit_ros_tree, render_visit_ros_pane
from .utilities import get_all_visit_ros, import_active_visit_ros


urlpatterns = patterns('',

################################################################################

                      url(r'add/$'  , 
                           visit_ros_add  , 
                           name="visit_ros_add_without_id"
                      ),

                      url(r'add/(?P<visit_id>\d+)/$'  , 
                           visit_ros_add  , 
                           name="visit_ros_add"
                       ),

                      url(r'json/$',
                           visit_ros_json, 
                           name="visit_ros_json_without_id"
                           ),

                      url(r'json/(?P<visit_id>\d+)/$',
                           visit_ros_json, 
                           name="visit_ros_json"
                           ),

                      #url(r'list/(?P<visit_id>\d+)/$' , 
                           #visit_ros_list , 
                           #name="visit_ros_list"
                       #),

                       url(r'ros/edit/$',
                           visit_ros_edit, 
                           name="visit_ros_edit_without_id"
                           ),

                       url(r'ros/edit/(?P<visit_ros_id>\d+)/$',
                           visit_ros_edit, 
                           name="visit_ros_edit"
                           ),

                       url(r'ros/del/$',
                           visit_ros_del, 
                           name="visit_ros_del_without_id"
                           ),

                       url(r'ros/del/(?P<visit_ros_id>\d+)/$',
                           visit_ros_del, 
                           name="visit_ros_del"
                           ),

                      url(r'ros/get_all_visit_ros/(?P<visit_id>\d+)/$',
                           get_all_visit_ros, 
                           name="get_all_visit_ros"
                           ),

                      #url(r'ros/import_active_visit_ros/(?P<visit_id>\d+)/$',
                           #import_active_visit_ros, 
                           #name="import_active_visit_ros"
                           #),

################################################################################

)