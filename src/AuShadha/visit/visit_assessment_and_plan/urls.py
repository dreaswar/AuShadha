from django.conf.urls import *
import AuShadha.settings

from .views import *
#from utilities import *

urlpatterns = patterns('',


            url(r'get/template/(?P<assessment_name>\w+)/(?P<visit_id>\d+)/$'  , 
                visit_assessment_and_plan_template , 
                name="visit_assessment_and_plan_template"
                ),

            url(r'get/visit_assessment_and_plan/(?P<visit_id>\d+)/$'  , 
                get_visit_assessment_and_plan, 
                name="get_visit_assessment_and_plan"
                ),

            url(r'json/(?P<visit_id>\d+)/$'  , 
                visit_assessment_and_plan_json , 
                name="visit_assessment_and_plan_json"
                ),

            #url(r'list/(?P<visit_id>\d+)/$' , 
                #visit_assessment_and_plan_list , 
                #name="visit_assessment_and_plan_list"
                #),

            url(r'add/(?P<visit_id>\d+)/$'  , 
                visit_assessment_and_plan_add , 
                name="visit_assessment_and_plan_add"
                ),


            url(r'edit/(?P<visit_assessment_and_plan_id>\d+)/$' , 
                visit_assessment_and_plan_edit , 
                name="visit_assessment_and_plan_edit"
                ),

            url(r'del/(?P<visit_assessment_and_plan_id>\d+)/$'  , 
                visit_assessment_and_plan_del  , 
                name="visit_assessment_and_plan_del"
                ),

)
