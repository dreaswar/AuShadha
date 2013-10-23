from django.conf.urls.defaults import *
from django.contrib import admin

import AuShadha.settings
from visit.views import *

admin.autodiscover()

urlpatterns = patterns('',

################################################################################

                      url(r'json/(?P<patient_id>\d+)/$'  , 
                          'visit.views.render_visit_json'  , 
                          name="render_visit_json"
                      ),

                      url(r'json/$', 
                          'visit.views.render_visit_json',
                          name='render_visit_json_without_id'
                      ),

                      url(r'render_visit_list/$', 
                          render_visit_list, 
                          name="render_visit_list"
                      ),

                      url(r'tree/(?P<patient_id>\d+)/$',
                          "visit.views.render_visit_tree", 
                          name="render_visit_tree"
                      ),

                      url(r'tree/$',
                          "visit.views.render_visit_tree", 
                          name="render_visit_tree_without_id"
                      ),

                       url(r'summary/(?P<patient_id>\d+)/$',
                           "visit.views.visit_summary", 
                           name="visit_summary"
                           ),

                       url(r'summary/$',
                           "visit.views.visit_summary", 
                           name="visit_summary_without_id"
                           ),

################################################################################

                       url(r'render_patient_visits_pdf/(?P<patient_id>\d+)/$',
                           'visit.views.render_patient_visits_pdf',
                           name='render_patient_visits_pdf'
                           ),

                       url(r'render_visit_pdf/(?P<patient_id>\d+)/$',
                           'visit.views.render_visit_pdf',
                           name='render_visit_pdf'
                           ),


################################################################################

                       url(r'detail/add/(?P<patient_id>\d+)/$',
                           visit_detail_add, 
                           name="visit_detail_add"
                           ),

                       url(r'detail/close/(?P<visit_id>\d+)/$',
                           visit_detail_close, 
                           name="visit_detail_close"
                           ),

                       url(r'detail/list/(?P<patient_id>\d+)/$',
                           visit_detail_list, 
                           name="visit_detail_list"),

                       url(r'detail/edit/(?P<visit_id>\d+)/$',
                           visit_detail_edit, 
                           name="visit_detail_edit"),

                       url(r'detail/del/(?P<visit_id>\d+)/$',
                           visit_detail_del, 
                           name="visit_detail_del"),

################################################################################

                       url(r'follow_up/add/(?P<visit_id>\d+)/$',
                           visit_follow_up_add, 
                           name="visit_follow_up_add"
                           ),

                       url(r'follow_up/add/$',
                           visit_follow_up_add, 
                           name="visit_follow_up_add_without_id"
                           ),

                       url(r'follow_up/edit/(?P<follow_up_id>\d+)/$',
                           visit_follow_up_edit, 
                           name="visit_follow_up_edit"
                           ),

                       url(r'follow_up/edit/$',
                           visit_follow_up_edit, 
                           name="visit_follow_up_edit_without_id"
                           ),


                       url(r'follow_up/del/(?P<follow_up_id>\d+)/$',
                           visit_follow_up_del, 
                           name="visit_follow_up_del"
                           ),

                       url(r'follow_up/del/$',
                           visit_follow_up_del, 
                           name="visit_follow_up_del_without_id"
                           ),

################################################################################

                       #url(r'complaint/add/(?P<id>\d+)/$'  , visit_complaint_add  , name="visit_complaint_add"),
                       #url(r'complaint/list/(?P<id>\d+)/$' , visit_complaint_list , name="visit_complaint_list"),

                       url(r'complaint/edit/(?P<complaint_id>\d+)/$',
                           visit_complaint_edit, 
                           name="visit_complaint_edit"),

                       url(r'complaint/del/(?P<complaint_id>\d+)/$',
                           visit_complaint_del, 
                           name="visit_complaint_del"
                           ),

################################################################################

                       #url(r'hpi/add/(?P<id>\d+)/$'  , visit_hpi_add  , name="visit_hpi_add"),
                       #url(r'hpi/list/(?P<id>\d+)/$' , visit_hpi_list , name="visit_hpi_list"),
                       #url(r'hpi/edit/(?P<id>\d+)/$' , visit_hpi_edit , name="visit_hpi_edit"),
                       #url(r'hpi/del/(?P<id>\d+)/$'  , visit_hpi_del  , name="visit_hpi_del"),

################################################################################

                       #url(r'past_history/add/(?P<id>\d+)/$'  , visit_past_history_add  , name="visit_past_history_add"),
                       #url(r'past_history/list/(?P<id>\d+)/$' , visit_past_history_list , name="visit_past_history_list"),
                       #url(r'past_history/edit/(?P<id>\d+)/$' , visit_past_history_edit , name="visit_past_history_edit"),
                       #url(r'past_history/del/(?P<id>\d+)/$'  , visit_past_history_del  , name="visit_past_history_del"),

################################################################################

                       #url(r'imaging/add/(?P<id>\d+)/$'  , visit_imaging_add  , name="visit_imaging_add"),
                       #url(r'imaging/list/(?P<id>\d+)/$' , visit_imaging_list , name="visit_imaging_list"),
                       #url(r'imaging/edit/(?P<id>\d+)/$' , visit_imaging_edit , name="visit_imaging_edit"),
                       #url(r'imaging/del/(?P<id>\d+)/$'  , visit_imaging_del  , name="visit_imaging_del"),

################################################################################

                       #url(r'inv/add/(?P<id>\d+)/$'  , visit_inv_add  , name="visit_inv_add"),
                       #url(r'inv/list/(?P<id>\d+)/$' , visit_inv_list , name="visit_inv_list"),
                       #url(r'inv/edit/(?P<id>\d+)/$' , visit_inv_edit , name="visit_inv_edit"),
                       #url(r'inv/del/(?P<id>\d+)/$'  , visit_inv_del  , name="visit_inv_del"),

################################################################################

                       #url(r'phyexam/add/(?P<id>\d+)/$'  , visit_phyexam_add  , name="visit_phyexam_add"),
                       #url(r'phyexam/list/(?P<id>\d+)/$' , visit_phyexam_list , name="visit_phyexam_list"),
                       #url(r'phyexam/edit/(?P<id>\d+)/$' , visit_phyexam_edit , name="visit_phyexam_edit"),
                       #url(r'phyexam/del/(?P<id>\d+)/$'  , visit_phyexam_del  , name="visit_phyexam_del"),

################################################################################

                       # url(r'(?P<exam_to_add>\w+)/add/(?P<id>\d+)/$'  ,exam_add , exam_add_with_id"),
                       # url(r'(?P<exam_to_add>\w+)/add/$'  ,exam_add ,
                       # exam_add_without_id"),

################################################################################

                       #url(r'phyexam/add/(?P<id>\d+)/$'  , visit_phyexam_add  , name="visit_phyexam_add"),
                       #url(r'phyexam/list/(?P<id>\d+)/$' , visit_phyexam_list , name="visit_phyexam_list"),
                       #url(r'phyexam/edit/(?P<id>\d+)/$' , visit_phyexam_edit , name="visit_phyexam_edit"),
                       #url(r'phyexam/del/(?P<id>\d+)/$'  , visit_phyexam_del  , name="visit_phyexam_del"),

################################################################################

                       url(r'add/(?P<patient_id>\d+)/$',
                           visit_detail_add, 
                           name="visit_add"
                           ),

                       url(r'add/$',
                           visit_detail_add, 
                           name="visit_add_without_id"
                           ),

                       url(r'list/(?P<patient_id>\d+)/$',
                           visit_detail_list, 
                           name="visit_list"
                           ),

                       url(r'edit/(?P<visit_id>\d+)/$',
                           visit_detail_edit, 
                           name="visit_edit"
                           ),
                       url(r'edit/$',
                           visit_detail_edit, 
                           name="visit_edit_without_id"
                           ),

                       url(r'close/(?P<visit_id>\d+)/$'       , 
                           visit_detail_close       , 
                           name="visit_close"
                           ),

                       url(r'close/$'       , 
                           visit_detail_close       , 
                           name="visit_close_without_id"
                           ),

                       url(r'del/(?P<visit_id>\d+)/$',
                           visit_detail_del, 
                           name="visit_del"
                           ),
                       url(r'del/$',
                           visit_detail_del, 
                           name="visit_del_without_id"
                           ),

)