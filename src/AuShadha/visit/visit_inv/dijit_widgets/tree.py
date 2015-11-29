# General Module imports-----------------------------------
from datetime import datetime, date, time
import yaml

# General Django Imports----------------------------------
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User

#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_protect
#from django.views.decorators.debug import sensitive_post_parameters
#from django.core import serializers
##from django.core.serializers import json
#from django.core.serializers.json import DjangoJSONEncoder

import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.views.dijit_tree import DijitTreeNode, DijitTree


class VisitTree(object):
    """
     Defines the Dijit UI for Visit Tree
    """

    def __init__(self, kwargs):
        self.request = kwargs['request']
        self.variables = kwargs

        try:
            f = open('visit/dijit_widgets/tree.yaml', 'r')
            self.yaml_file = yaml.load(f)
            f.close()

        except IOError:
            raise Exception("Input Output Error ! ")

        try:
            self.user = self.request.user

        except(AttributeError, ValueError, NameError, TypeError):
            raise Exception("Invalid User or no user supplied")

    def __unicode__(self):
        return self.__call__()

    def __call__(self):

        y = self.yaml_file

        visit_tree_node = DijitTree()

        if not getattr(self.variables['patient'], 'urls', None):
            self.variables['patient'].save()

        if self.variables['can_add_new_visit']:
            new_visit_yaml = y['new_visit'].copy()
            new_visit_yaml['ondblclick'] = self.variables[
                'patient'].urls['add']['visit']
            new_visit_yaml['onclick'] = self.variables[
                'patient'].urls['add']['visit']
            new_visit_node = DijitTreeNode(new_visit_yaml)
            visit_tree_node.add_child_node(new_visit_node)

        if self.variables['all_visits']:
            visit_node = DijitTreeNode(y['visits'])
            all_visits = self.variables['all_visits']

            if self.variables['active_visits']:
                active_visits = self.variables['active_visits']
                active_visits_node = DijitTreeNode(y['active_visits'])

                for active_visit in active_visits:
                    if not getattr(active_visit, 'urls', None):
                        active_visit.save()
                    active_visit_yaml = y['active_visit'].copy()
                    #close_active_visit_yaml = y['close_active_visit'].copy()
                    add_follow_up_visit_yaml = y[
                        'add_follow_up_to_active_visit'].copy()

                    active_visit_yaml['id'] = "%s_%s" % (
                        active_visit_yaml['id'], str(active_visit.id))
                    active_visit_yaml['name'] = "%s (%s)" % (
                        active_visit_yaml['name'], active_visit.visit_date.date().isoformat())
                    active_visit_yaml['ondblclick'] = active_visit.urls['edit']
                    active_visit_yaml['onclick'] = active_visit.urls['edit']

                    #close_active_visit_yaml['id'] = "%s_%s" %(close_active_visit_yaml['id'], str(active_visit.id) )
                    add_follow_up_visit_yaml['id'] = "%s_%s" % (
                        add_follow_up_visit_yaml['id'], str(active_visit.id))
                    #close_active_visit_yaml['ondblclick'] = active_visit.get_visit_detail_close_url()
                    add_follow_up_visit_yaml[
                        'ondblclick'] = active_visit.urls['add']['follow_up']

                    active_visit_node = DijitTreeNode(active_visit_yaml)

                    #close_active_visit_node = DijitTreeNode(close_active_visit_yaml)
                    # active_visit_node.add_child_node(close_active_visit_node)

                    add_follow_up_active_visit_node = DijitTreeNode(
                        add_follow_up_visit_yaml)
                    active_visit_node.add_child_node(
                        add_follow_up_active_visit_node)

                    fu = active_visit.has_fu_visits()

                    if fu:
                        fu_active_visits_yaml = y[
                            'active_visits_follow_ups'].copy()
                        fu_active_visits_yaml['id'] = "%s_%s" % (
                            active_visit_yaml['id'], str(active_visit.id))
                        active_visit_followup_visits_node = DijitTreeNode(
                            fu_active_visits_yaml)

                        for f in fu:
                            if not getattr(f, 'urls', None):
                                f.save()
                            print "*" * 100
                            print f.urls
                            print "*" * 100
                            f_yaml = y['active_visit_follow_up'].copy()
                            f_yaml['id'] = "%s_%s" % (f_yaml['id'], str(f.id))
                            f_yaml['ondblclick'] = f.urls['edit']
                            f_yaml['onclick'] = f.urls['edit']
                            active_visit_followup_visit_node = DijitTreeNode(
                                f_yaml)
                            active_visit_followup_visits_node.add_child_node(
                                active_visit_followup_visit_node)

                        active_visit_node.add_child_node(
                            active_visit_followup_visits_node)

                    active_visits_node.add_child_node(active_visit_node)

                visit_node.add_child_node(active_visits_node)

            if self.variables['inactive_visits']:
                inactive_visits = self.variables['inactive_visits']
                inactive_visits_node = DijitTreeNode(y['previous_visits'])
                visit_node.add_child_node(inactive_visits_node)

                for inactive_visit in inactive_visits:
                    if not getattr(inactive_visit, 'urls', None):
                        inactive_visit.save()

                    prev_v_yaml = y['previous_visit'].copy()
                    prev_v_yaml['id'] = "%s_%s" % (
                        prev_v_yaml['id'], str(inactive_visit.id))
                    prev_v_yaml['name'] = "%s (%s)" % (
                        prev_v_yaml['name'], inactive_visit.visit_date.date().isoformat())
                    prev_v_yaml['onclick'] = inactive_visit.urls['edit']
                    prev_v_yaml['ondblclick'] = inactive_visit.urls['edit']

                    inactive_visit_node = DijitTreeNode(prev_v_yaml)
                    inactive_visits_node.add_child_node(inactive_visit_node)

                    prev_fu = inactive_visit.has_fu_visits()
                    if prev_fu:
                        prev_fu_yaml = y['previous_visits_follow_ups'].copy()
                        prev_fu_yaml['id'] = "%s_%s" % (
                            prev_fu_yaml['id'], str(inactive_visit.id))
                        inactive_visit_followup_visits_node = DijitTreeNode(
                            prev_fu_yaml)
                        inactive_visit_node.add_child_node(
                            inactive_visit_followup_visits_node)

                        for fu in prev_fu:
                            if not getattr(fu, 'urls', None):
                                fu.save()
                            fu_yaml = y['previous_visit_follow_up'].copy()
                            fu_yaml['id'] = "%s_%s" % (
                                fu_yaml['id'], str(fu.id))
                            fu_yaml['name'] = "%s (%s)" % (
                                fu_yaml['name'], fu.visit_date.date().isoformat())
                            fu_yaml['ondblclick'] = fu.urls['edit']
                            fu_yaml['onclick'] = fu.urls['edit']

                            inactive_visit_followup_visit_node = DijitTreeNode(
                                fu_yaml)
                            inactive_visit_followup_visits_node.add_child_node(
                                inactive_visit_followup_visit_node)

            visit_tree_node.add_child_node(visit_node)

        history_node = DijitTreeNode(y['history'])
        visit_tree_node.add_child_node(history_node)

        medication_list_node = DijitTreeNode(y['medications'])
        visit_tree_node.add_child_node(medication_list_node)

        preventives_node = DijitTreeNode(y['preventives'])
        visit_tree_node.add_child_node(preventives_node)

        investigation_node = DijitTreeNode(y['investigation'])
        visit_tree_node.add_child_node(investigation_node)

        imaging_node = DijitTreeNode(y['imaging'])
        visit_tree_node.add_child_node(imaging_node)

        procedures_node = DijitTreeNode(y['procedures'])
        visit_tree_node.add_child_node(procedures_node)

        jsondata = visit_tree_node.to_json()
        return json
