from django.conf.urls.defaults import *

import AuShadha.settings
from visit.views import *
#from admission.views import *
from phyexam.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

                       #url(r'phyexam/add/(?P<id>\d+)/$'  , visit_phyexam_add  , name="visit_phyexam_add"),
                       #url(r'phyexam/list/(?P<id>\d+)/$' , visit_phyexam_list , name="visit_phyexam_list"),
                       #url(r'phyexam/edit/(?P<id>\d+)/$' , visit_phyexam_edit , name="visit_phyexam_edit"),
                       #url(r'phyexam/del/(?P<id>\d+)/$'  , visit_phyexam_del  , name="visit_phyexam_del"),

            url(r'vascular_exam/add/(?P<id>\d+)/$'  , 
                vascular_exam_add  , 
                name="vascular_exam_add"
                ),
            url(r'vascular_exam/list/(?P<id>\d+)/$' , 
                vascular_exam_list , 
                name="vascular_exam_list"
                ),
            url(r'vascular_exam/edit/(?P<id>\d+)/$' , 
                vascular_exam_edit , 
                name="vascular_exam_edit"
                ),
            url(r'vascular_exam/del/(?P<id>\d+)/$'  , 
                vascular_exam_del  , 
                name="vascular_exam_del"
                ),

)
