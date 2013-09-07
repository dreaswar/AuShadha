from phy_exam_constants import PC, validator_factory

class PhyExamBasePresentationClass(object):

    """
      Creates a Class Based Representation of Physical Examination Object for manipulation
      and HTML Formatting.
    """

    fields = []
    field_names = []
    field_map = {}

    templates = {'add' :'', 'edit':'', 'list':'', 'object': ''}

    def __init__(self, exam_instance, request=None, context=None):
        self.exam = exam_instance
        self.__model_label__ = self.exam.__model_label__
        self.__app_label__ = self.exam._meta.app_label
        self._meta = self.exam._meta

        if self.__model_label__ in PC.keys():
          self.field_map = PC[self.__model_label__]
        else:
          raise Exception("""
                            Invalid Model Supplied. 
                            This does not have a Presentation Model Registered.
                          """
                          )

        for field in self._meta.fields:
            try:
                self.fields.append(field)
                self.field_names.append(field.name)
                try:
                  f = self.field_map[field.name]
                  f['value'] = field.value_from_object(self.exam)
                  f_validator = f['validator']
                  f_constraints = f['constraints']
                  f_compare_with  = f['default']

                  #print "Calling Factory Validator with Validator: ", f_validator
                  #print "Calling Factory Validator with Value of : ", f['value']
                  #print "Calling Factory Validator with Constraints: ", f_constraints
                  #print "Calling Factory Validator with Compare with: ", f_compare_with

                  f['is_abnormal'] = validator_factory(f_validator,
                                                      f['value'],
                                                      f_constraints,
                                                      f_compare_with)
                except (KeyError,NameError,ValueError):
                  continue
            except(AttributeError):
                print "AttributeError Raised...."
                continue

    def __call__(self):
        return self.build_html_div()

    def __unicode__(self):
        return self.__call__()

    # def template_render(self):
        # try:
            # self.templates.object.render()
        # except('TemplateDoesNotExist'):
            # return None

    def build_html_div(self):

        paragraph = ''
        for v in self.field_map.values():
            html_class = ''
            label = unicode(v['label'])
            value = v['value']
            if value:
                value = unicode(value)
                unit = unicode(v['unit'])
                delimitter = unicode(v['delimitter'])
                is_abnormal = v['is_abnormal']
                if is_abnormal:
                    html_class = 'abnormal_value_indicator_text'
            else:
                value = unicode("--Not Recorded--")
                unit = unicode('')
                delimitter = unicode('')
                html_class = 'suggestion_text'
            line = """<p> <span class='label_text'>%s:</span> 
                          <span> %s %s %s </span>
                          <span class="%s">  </span> 
                      </p>
                   """ % (label,value, delimitter, unit, html_class)
            paragraph += line
        return """<div> %s </div>""" % (paragraph)

    def build_html_table(self):
        pass

    def return_object_json(self):
        pass

    def return_object_grid_structure(self):
        pass



class VisitComplaintsPresentationClass(PhyExamBasePresentationClass):

    """
      Creates a Class Based Representation of Visit Complaints for manipulation
      and HTML Formatting.
    """

    # templates = {
                            #'add' :get_template('visit/complaints/add.html'),
                            #'edit':get_template('visit/complaints/edit.html'),
                            #'list':get_template('visit/complaints/list.html'),
                            #'object': get_template('visit/complaints/complaint.html')
                            #}

    # def template_render(self):
        # try:
            # self.templates.object.render()
        # except('TemplateDoesNotExist'):
            # return None


class VisitHPIPresentationClass(PhyExamBasePresentationClass):

    """
      Creates a Class Based Representation of Visit HPI
      and HTML Formatting.
    """

    # templates = {
                            #'add' :get_template('visit/hpi/add.html'),
                            #'edit':get_template('visit/hpi/edit.html'),
                            #'list':get_template('visit/hpi/list.html'),
                            #'object': get_template('visit/hpi/hpi.html')
                            #}

    # def template_render(self):
        # try:
            # self.templates.object.render()
        # except('TemplateDoesNotExist'):
            # return None

class VitalExamObjPresentationClass(PhyExamBasePresentationClass):

    """
      Creates a Class Based Representation of Vital Object for manipulation
      and HTML Formatting.
    """

    # templates = {
                            #'add' :get_template('phyexam/vitals/add.html'),
                            #'edit':get_template('phyexam/vitals/edit.html'),
                            #'list':get_template('phyexam/vitals/list.html'),
                            #'object': get_template('phyexam/vitals/vital.html')
                            #}

    # def template_render(self):
        # try:
            # self.templates.object.render()
        # except('TemplateDoesNotExist'):
            # return None

class GenExamObjPresentationClass(PhyExamBasePresentationClass):

    """
      Creates a Class Based Representation of Vital Object for manipulation
      and HTML Formatting.
    """

    # templates = {
                            #'add' :get_template('phyexam/gen_exam/add.html'),
                            #'edit':get_template('phyexam/gen_exam/edit.html'),
                            #'list':get_template('phyexam/gen_exam/list.html'),
                            #'object': get_template('phyexam/gen_exam/gen_exam.html')
                            #}

    # def template_render(self):
        # try:
            # self.templates.object.render()
        # except('TemplateDoesNotExist'):
            # return None


class SysExamObjPresentationClass(PhyExamBasePresentationClass):

    """
      Creates a Class Based Representation of Vital Object for manipulation
      and HTML Formatting.
    """

    # templates = {
                            #'add' :get_template('phyexam/sys_exam/add.html'),
                            #'edit':get_template('phyexam/sys_exam/edit.html'),
                            #'list':get_template('phyexam/sys_exam/list.html'),
                            #'object': get_template('phyexam/sys_exam/sys_exam.html')
                            #}

    # def template_render(self):
        # try:
            # self.templates.object.render()
        # except('TemplateDoesNotExist'):
            # return None

class PeriNeuroExamObjPresentationClass(PhyExamBasePresentationClass):

    """
      Creates a Class Based Representation of Vital Object for manipulation
      and HTML Formatting.
    """

    # templates = {
                            #'add' :get_template('phyexam/neuro_exam/add.html'),
                            #'edit':get_template('phyexam/neuro_exam/edit.html'),
                            #'list':get_template('phyexam/neuro_exam/list.html'),
                            #'object': get_template('phyexam/neuro_exam/neuro_exam.html')
                            #}

    # def template_render(self):
        # try:
            # self.templates.object.render()
        # except('TemplateDoesNotExist'):
            # return None

class VascExamObjPresentationClass(PhyExamBasePresentationClass):

    """
      Creates a Class Based Representation of Vital Object for manipulation
      and HTML Formatting.
    """

    # templates = {
                            #'add' :get_template('phyexam/vasc_exam/add.html'),
                            #'edit':get_template('phyexam/vasc_exam/edit.html'),
                            #'list':get_template('phyexam/vasc_exam/list.html'),
                            #'object': get_template('phyexam/vasc_exam/vasc_exam.html')
                            #}

    # def template_render(self):
        # try:
            # self.templates.object.render()
        # except('TemplateDoesNotExist'):
            # return None


########################## Factory Functions...##################################

def vitalexamobjpresentationclass_factory(instance):
  return VitalExamObjPresentationClass(instance)

def genexamobjpresentationclass_factory(instance):
  return GenExamObjPresentationClass(instance)

def sysexamobjpresentationclass_factory(instance):
  return GenExamObjPresentationClass(instance)

def neuroexamobjpresentationclass_factory(instance):
  return PeriNeuroExamObjPresentationClass(instance)

def vascexamobjpresentationclass_factory(instance):
  return VascExamObjPresentationClass(instance).__call__()

def vascexamobjpresentationclass_querysetfactory(queryset):
  html = '<div>'
  for instance in queryset:
    h = vascexamobjpresentationclass_factory(instance)
    html += h
    html += '</div>'
  return html