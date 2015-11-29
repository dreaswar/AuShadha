# General Module imports-----------------------------------
from datetime import datetime, date, time
import yaml

# General Django Imports-----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import Template, Context
import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree


class SocialHistoryTree(object):

    """
     Defines the Dijit UI for SocialHistoryTree
    """

    def __init__(self, kwargs):

        self.request = kwargs['request']
        self.variables = RequestContext(self.request, kwargs)
        if not getattr(self.variables['patient_detail_obj'], 'urls', None):
            self.variables['patient_detail_obj'].save()

        try:
            d = open('history/social_history/dijit_widgets/tree.yaml', 'r')
            f = d.read()
            d.close()
            pane_template = Template(f)
            rendered_pane = pane_template.render(self.variables)
            self.yaml_file = yaml.load(rendered_pane)

        except(IOError):
            raise Http404("No template file to render the pane ! ")

        try:
            self.user = self.request.user

        except(AttributeError, ValueError, NameError, TypeError):
            raise Exception("Invalid User or no user supplied")

    def __unicode__(self):
        return self.__call__()

    def __call__(self):

        y = self.yaml_file
        tree_node = DijitTree()
        # Render the Nodes here..
        jsondata = tree_node.to_json()
        return json
