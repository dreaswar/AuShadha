from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings
admin.autodiscover()

from .views import icd10_chapter_json, get_sections_for_chapter, get_diagnosis_for_section, icd10_diagnosis_search
from .dijit_widgets.pane import render_icd10_pane
from .dijit_widgets.tree import render_icd10_tree

urlpatterns = patterns('',
                       url( r'/get/sections/(?P<chapter_id>\d+)/(?P<output>\w+)/$', get_sections_for_chapter, name="get_sections_for_chapter" ),
                       url( r'/get/diagnosis/(?P<section_id>\d+)/(?P<output>\w+)/$', get_diagnosis_for_section, name="get_diagnosis_for_section" ),

                       url( r'pane/$', render_icd10_pane, name='render_icd10_pane' ),
                       url( r'tree/$', render_icd10_tree, name="render_icd10_tree" ),
                       url( r'diagnosis/search/$', icd10_diagnosis_search, name="icd10_diagnosis_search" ),

                       url( r'chapter/json/$', icd10_chapter_json, name="icd10_chapter_json" ),
)
