from django.conf.urls.defaults import *
#from django.contrib import admin
#admin.autodiscover()

import AuShadha.settings

from .views import *
#from .dijit_widgets.pane import render_visit_tree, render_visit_pane
from .utilities import get_all_patient_complaints, import_active_complaints


urlpatterns = patterns('',

################################################################################

                       url(r'add/(?P<visit_id>\d+)/$'  , 
                           visit_complaint_add  , 
                           name="visit_complaint_add"
                       ),

                      url(r'json/(?P<visit_id>\d+)/$',
                           visit_complaint_json, 
                           name="visit_complaint_json"
                           ),

                      url(r'json/$',
                           visit_complaint_json, 
                           name="visit_complaint_json_without_id"
                           ),

                      #url(r'list/(?P<visit_id>\d+)/$' , 
                           #visit_complaint_list , 
                           #name="visit_complaint_list"
                       #),

                       url(r'complaint/edit/(?P<visit_complaint_id>\d+)/$',
                           visit_complaint_edit, 
                           name="visit_complaint_edit"),

                       url(r'complaint/del/(?P<visit_complaint_id>\d+)/$',
                           visit_complaint_del, 
                           name="visit_complaint_del"
                           ),

                      url(r'complaint/get/(?P<visit_id>\d+)/$',
                           get_all_patient_complaints, 
                           name="get_all_patient_complaints"
                           ),

                      url(r'complaint/import_active_complaints/(?P<visit_id>\d+)/$',
                           import_active_complaints, 
                           name="import_active_complaints"
                           ),

################################################################################

)