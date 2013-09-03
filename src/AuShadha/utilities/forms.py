#UTILITIES

class AuModelFormErrorFormatter(object):
  """
    Generic Form Error Formatter
  """
  def __init__(self,form):
    self.form = form
    self.content = ''
    self.form_name = getattr(self.form,'__form_name__','Form Error')
    #return self.__unicode__()
  
  def __unicode__(self):
    if self.form.errors:
      error_header = "<h3 class='suggestion_text'>Error in: "
      error_header += self.form_name
      error_header += "</h3>"
      self.content += error_header
      i=1
      for k,v in self.form.errors.items():
        self.content += "<p>%s) at field name '%s' %s</span> </p>" %(i,k,v)
        i += 1
    return self.content
# error formatter factory
def aumodelformerrorformatter_factory(form):
  form_error = AuModelFormErrorFormatter(form)
  return form_error.__unicode__()
