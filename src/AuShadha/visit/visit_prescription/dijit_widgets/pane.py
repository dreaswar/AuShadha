##########################################################################
# Project: AuShadha
# Description: Pane of the UI for visit_prescription
# Author ; Dr.Easwar T.R
# Date: 04-11-2013
# License: GNU-GPL Version3, see LICENSE.txt for details
##########################################################################

from cStringIO import StringIO
import yaml

# General Django Imports----------------------------------
from django.http import Http404, HttpResponse
import json
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.contrib.auth.decorators import login_required

from visit.visit_prescription import MODULE_LABEL
from visit.visit_prescription.models import VisitPrescription

from visit.visit.models import VisitDetail


@login_required
def render_visit_prescription_pane(request, visit_detail_id=None):

    if request.method == 'GET' and request.is_ajax():
        try:
            if visit_detail_id:
                visit_detail_id = int(visit_detail_id)
            else:
                visit_detail_id = int(request.GET.get('visit_detail_id'))

            app_wrapper = []
            visit_detail_obj = VisitDetail.objects.get(pk=visit_detail_id)

            if not getattr(visit_detail_obj, 'urls', None):
                print "No Attribute of URLS on Patient. Saving to generate the same"
                visit_detail_obj.save()
            context = Context(
                {'visit_detail_id': visit_detail_id, 'visit_detail_obj': visit_detail_obj})

            try:
                pane_template = Template(
                    open(
                        'visit/visit_prescription/dijit_widgets/pane.yaml',
                        'r').read())
            except(IOError):
                raise Http404("No template file to render the pane ! ")

            rendered_pane = pane_template.render(context)
            pane_yaml = yaml.load(rendered_pane)
            app_object = {}
            app_object['app'] = MODULE_LABEL
            app_object['ui_sections'] = {
                'app_type': 'sub_module',
                'load_after': ['visit'],
                'load_first': False,
                'layout': [],
                'widgets': {'tree': None,
                            'summary': None,
                            'grid': None,
                            'search': None
                            }
            }
            app_object['url'] = None
            app_wrapper.append(app_object)
            success = True
            error_message = "Returning " + MODULE_LABEL + " app pane variables"
            data = {
                'success': success,
                'error_message': error_message,
                'app': app_wrapper,
                'pane': pane_yaml}
            jsondata = json.dumps(data)
            return HttpResponse(jsondata, content_type="application/json")

        except (TypeError, NameError, ValueError, AttributeError, KeyError):
            raise Http404("Bad Request Parameters")
        except (VisitDetail.DoesNotExist):
            raise Http404("Bad Request: Visit Does Not Exist")

    else:
        raise Http404("Bad Request Method")
