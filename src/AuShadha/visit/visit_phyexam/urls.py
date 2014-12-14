################################################################################
#
#
#
################################################################################


from django.conf.urls import *
import AuShadha.settings

from .views import *
#from utilities import *

urlpatterns = patterns( '',

            url(r'get/template/(?P<exam_name>\w+)/(?P<visit_id>\d+)/$'  , 
                visit_phyexam_template , 
                name="visit_phyexam_template"
            ),

            url(r'json/(?P<exam_name>\w+)/(?P<visit_id>\d+)/$'  , 
                visit_phyexam_json , 
                name="visit_phyexam_json"
            ),

            url(r'list/(?P<exam_name>\w+)/(?P<visit_id>\d+)/$' , 
                visit_phyexam_list , 
                name="visit_phyexam_list"
            ),

            url(r'add/(?P<exam_name>\w+)/(?P<visit_id>\d+)/$'  , 
                visit_phyexam_add , 
                name="visit_phyexam_add"
            ),

            url(r'edit/(?P<exam_name>\w+)/(?P<visit_phyexam_id>\d+)/$' , 
                visit_phyexam_edit , 
                name="visit_phyexam_edit"
            ),

            url(r'del/(?P<exam_name>\w+)/(?P<visit_phyexam_id>\d+)/$'  , 
                visit_phyexam_del  , 
                name="visit_phyexam_del"
            ),
)
