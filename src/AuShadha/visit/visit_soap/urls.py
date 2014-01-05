from django.conf.urls.defaults import *
import AuShadha.settings

from .views import *
#from utilities import *

urlpatterns = patterns('',


            url(r'get/template/(?P<soap_name>\w+)/(?P<visit_id>\d+)/$'  , 
                visit_soap_template , 
                name="visit_soap_template"
                ),

            url(r'get/visit_soap/(?P<visit_id>\d+)/$'  , 
                get_visit_soap, 
                name="get_visit_soap"
                ),

            url(r'json/(?P<visit_id>\d+)/$'  , 
                visit_soap_json , 
                name="visit_soap_json"
                ),

            #url(r'list/(?P<visit_id>\d+)/$' , 
                #visit_soap_list , 
                #name="visit_soap_list"
                #),

            url(r'add/(?P<visit_id>\d+)/$'  , 
                visit_soap_add , 
                name="visit_soap_add"
                ),


            url(r'edit/(?P<visit_soap_id>\d+)/$' , 
                visit_soap_edit , 
                name="visit_soap_edit"
                ),

            url(r'del/(?P<visit_soap_id>\d+)/$'  , 
                visit_soap_del  , 
                name="visit_soap_del"
                ),

)
