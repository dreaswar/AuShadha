from django.conf.urls import *
from django.contrib import admin

import AuShadha.settings
admin.autodiscover()

from dijit_widgets.pane import render_drugbankcadrugs_pane
from dijit_widgets.tree import render_drugbankcadrugs_tree
from .views import drugbankcadrugs_json_for_a_drug,\
                   drugbankcadrugs_summary_by_drug_id,\
                   drugbankcadrugs_summary_by_drug_name,\
                   drugbankcadrugs_search, \
                   drugbankcadrugs_search_by_drug_name, \
                   get_drugbankca_publications


urlpatterns = patterns('',

	url(r'get/publications/$', 
            get_drugbankca_publications, 
            name = 'get_drugbankca_publications'
           ),

	url(r'render/pane/$', 
            render_drugbankcadrugs_pane, 
            name = 'render_drugbankcadrugs_pane'
           ),

	url(r'render/tree/$', 
            render_drugbankcadrugs_tree, 
            name = 'render_drugbankcadrugs_tree'
           ),

	url(r'json/(?P<drug_id>\d+)/$', 
            drugbankcadrugs_json_for_a_drug, 
            name = 'drugbankcadrugs_json_for_a_drug'
          ),

	url(r'summary/by_drug_id/(?P<drug_id>\d+)/$', 
            drugbankcadrugs_summary_by_drug_id, 
            name = 'drugbankcadrugs_summary_by_drug_id'
          ),

	url(r'summary/by_drug_name/$', 
            drugbankcadrugs_summary_by_drug_name, 
            name = 'drugbankcadrugs_summary_by_drug_name'
          ),

	url(r'search/$', 
            drugbankcadrugs_search, 
            name = 'drugbankcadrugs_search'
          ),

        url(r'search_by_drug_name/$', 
            drugbankcadrugs_search_by_drug_name, 
            name = 'drugbankcadrugs_search_by_drug_name'
          ),

)


