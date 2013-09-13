################################################################################
# Presentation classes for AuShadhaModels.
# 
# This will format, pass validation output and generate HTML, JSON ouputs
# This is attempt to make something simple rather than use Django Class based
#   views.
#
# Author: Dr.Easwar T.R
# License: GNU-GPL Version 3
# Date : 09-09-2013
################################################################################


from phy_exam_constants import PC
from validator import validator_factory

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
                  f['class_name'] = field.__class__.__name__
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
                  #print "Validator returned: " , f['is_abnormal']
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
            class_name = v['class_name']
            is_abnormal = v['is_abnormal']
            if value:
                if class_name == "BooleanField": 
                  value = unicode("Present")
                  delimitter = ''
                  unit = ''
                else:
                  value = unicode(value)
                  unit = unicode(v['unit'])
                  delimitter = unicode(v['delimitter'])
                if is_abnormal:
                    html_class = 'abnormal_value_indicator_text'
            else:
                if class_name == "BooleanField":
                  value = unicode("Not Present")
                  html_class = ''
                else:
                  value = unicode("--Not Recorded--")
                  html_class = 'suggestion_text'
                unit = unicode('')
                delimitter = unicode('')

            line = """<p> <span class='label_text'>%s:</span> 
                          <span class="%s">%s %s %s  </span> 
                      </p>
                   """ % (label, html_class,value, delimitter, unit)
            paragraph += line
        return """<div> %s </div>""" % (paragraph)

    def build_table_header(self):
        header = ''
        for k in self.field_map.values():
          label = unicode(k['label'])
          header += '<th>'+label+'</th>'
        return "<thead> <tr> %s </th> </thead>" %(header)

    def build_table_rows(self):
        line = ''
        for v in self.field_map.values():
          html_class = ''
          label = unicode(v['label'])
          value = v['value']
          class_name = v['class_name']
          is_abnormal = v['is_abnormal']
          if value:
              if class_name is not "BooleanField":
                value= unicode(value)
                unit = unicode(v['unit'])
                delimitter = unicode(v['delimitter'])                
              else:
                value = "Present"
                unit = ''
                delimitter = ' '
              if is_abnormal:
                  html_class = 'abnormal_value_indicator_text'
          else:
              if class_name is not "BooleanField":
                value = unicode("--Not Recorded--")
                html_class = 'suggestion_text'
              else:
                value = unicode("Not Present")
                html_class = ''
              unit = unicode('')
              delimitter = unicode('')

          line += """<td class='%s'>%s %s %s</td>
                  """ %(html_class, value, delimitter, unit)
        return "<tr > %s </tr>" %(line)


    def build_html_table(self):

        header = '<thead> <tr>'
        for k in self.field_map.keys():
          header += '<th>'+k+'</th>'
        header += '</tr></thead>'

        body = '<tbody>'
        for v in self.field_map.values():
            row = '<tr>'
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
            line = """<td class='label_text'>%s:</td> 
                      <td class="%s">%s</td>
                      <td> %s  </td>
                      <td> %s  </td> 
                   """ % (label, html_class,value, delimitter, unit)
            row += (line+'</tr>')
            body += row
        return """<table class='content_pane_table'> %s %s </table>""" % (header,body)

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

class VisitROSPresentationClass(PhyExamBasePresentationClass):

    """
      Creates a Class Based Representation of Visit ROS
      and HTML Formatting.
    """

    # templates = {
                            #'add' :get_template('visit/ros/add.html'),
                            #'edit':get_template('visit/ros/edit.html'),
                            #'list':get_template('visit/ros/list.html'),
                            #'object': get_template('visit/ros/ros.html')
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

def visitrospresentationclass_factory(instance):
  return VisitROSPresentationClass(instance)()

def vitalexamobjpresentationclass_factory(instance):
  return VitalExamObjPresentationClass(instance)()

def genexamobjpresentationclass_factory(instance):
  return GenExamObjPresentationClass(instance)()

def sysexamobjpresentationclass_factory(instance):
  return GenExamObjPresentationClass(instance)()

def neuroexamobjpresentationclass_factory(instance):
  return PeriNeuroExamObjPresentationClass(instance)()

def vascexamobjpresentationclass_factory(instance):
  v = VascExamObjPresentationClass(instance)
  return v

def vascexamobjpresentationclass_querysetfactory(queryset):
  h_head = ''
  h_rows = ''
  for instance in queryset:
    h = vascexamobjpresentationclass_factory(instance)
    if not h_head:
      h_head = h.build_table_header()
    h_rows += h.build_table_rows()
  return "<table class='content_pane_table'> %s <tbody> %s </tbody> </table>" %( h_head,h_rows)