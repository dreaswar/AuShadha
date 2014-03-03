################################################################################
# 
# This is a ' Experimental Effort ' to do something like Django Class Based Views.
#
# Eventually I hope to do something Generic Class Based Views dont. Something
#   specific to AuShadha .....
#
# visit.visit_phyexam.presentation_classes.PhyExamBasePresentationClass was a sandbox 
#   which works well. 
#
# This is an attempt to make it Project wide. PhyExamBasePresentationClass
#   has been imported here just to extend it. Actually when it is implemented fully,
#   this will be the base class
#
#################################################################################

import json
import datetime
from django.core.serializers.json import Serializer, Deserializer, DjangoJSONEncoder

from phyexam.models import DEFAULT_VITALS
from phyexam.phy_exam_constants import PC
from phyexam.presentation_classes import PhyExamBasePresentationClass
from phyexam.validator import Validator,validator_factory
from AuShadha.utilities.forms import AuModelFormErrorFormatter,aumodelformerrorformatter_factory

class SingleModelInstanceView(object):

    """
      Creates a Class Based Representation of Single Model Instance for
      manipulation and HTML Formatting.

      This is used for HTML, JSON, XML generation and Formatting.

      Subclasses can generate appropriate HTML forms with Dijit Widgets and do validation.

      Template rendering is done and rendered templates are stored as instance attributes.

    """

    unit_delimitter_map = {}
    fields = []
    field_names = []
    field_map = {}

    # Put template paths here as get_template objects.
    templates = {
        'add': '',
        'edit': '',
                'list': '',
                'object': '',
                'json': '',
                'xml': '',
                'csv': '',
                'pdf': ''
    }

    def __init__(self,
                 model_instance,
                 form=None,
                 formset=None,
                 request=None,
                 context=None):

        self.instance = model_instance
        self.__model_label__ = self.instance.__model_label__
        self.__app_label__ = self.instance._meta.app_label
        self._meta = self.instance._meta

        for field in self.instance._meta.fields:
            try:
                field_name = field.name
                field_val = field.value_from_object(self.instance)
                self.fields.append(field)
                self.field_names.append(field_name)
            except(AttributeError):
                print "AttributeError Raised...."
                continue

    def __call__(self):
        return self.build_html_div()

    def __unicode__(self):
        return self.__call__()

    # Template setting, getting, Rendering
    def set_template(self, template_action, path):
        """Sets Template with a given action and Path."""
        try:
            self.template[unicode(template_action)] = get_template(path)
            return True
        except (TemplateDoesNotExist):
            raise Exception("Requested Template Does not Exist ! ")

    def get_template(self, template_action):
        """Gets Template with a given action and Path.

        If not set Returns None

        """
        try:
            t = self.template[unicode(template_action)]
            if t:
                return t
            else:
                return None
        except (KeyError):
            raise Exception("No Such template action.")

    def template_render(self, template_action, request):
        try:
            t = self.templates[template_action]
            c = request.context
            if t and c:
                t.render(c)
            else:
                raise Exception(
                    "Template / Request Value Cannot be Null. Nothing to Render!")
        except('TemplateDoesNotExist'):
            raise Exception("Template Does not Exist")
        except(KeyError):
            raise Exception("No such Template Action")

    # Request Handling
    def get(self, request):
        """Routes all GET Request to absolute URLS."""
        pass

    def post(self, request):
        """Routes all POST Request to absolute URLS."""
        pass

    # Value Evaluation and Presentation CSS Classes
    def _eval(self, value, name):
        """Implements a Validation methods for values in field map.

        This is useful for generating CSS classes for HTML Presentation

        """
        pass

    # Building HTML
    def build_html_div(self):
        """Returns an HTML Formatted Version of the Model wrapped in a Div.

        Custom CSS classes Validation can be done here using self._eval
        for each value If you dont want to use this way of HTML building
        there is always the self.template_render method

        """
        pass

    def build_html_table(self):
        """Returns an HTML Formatted Version of the Model wrapped in a Table.

        Custom CSS classes Validation can be done here using self._eval
        for each value If you dont want to use this way of HTML building
        there is always the self.template_render method

        """
        pass

    # Serialisation
    def return_object_json(self):
        """Returns an JSON Version of the Model Instance."""
        pass

    def return_object_grid_structure(self):
        """Returns the Grid Structure to use for Dojo Grid."""
        pass


class QuerySetGenericView(object):
    pass
