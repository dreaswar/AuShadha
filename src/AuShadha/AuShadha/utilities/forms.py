################################################################################
# Description : AuShadha Base ModelForm and Several Form Utilities
# Author      : Dr. Easwar T.R
# Date        : 16-09-2013
# License     : Part of AuShadha Project. Licensed under GNU-GPL Version 3
#                Please see AuShadha/LICENSE 
################################################################################

"""
 Defines a generic AuShadhaModelForm error formatter and its factory
 Returns a well formatted error_message on Form Submit errors
 with relevent CSS styles.
"""

class AuModelFormErrorFormatter(object):

    """
    Generic Form Error Formatter.
    """

    def __init__(self, form):
        self.form = form
        self.content = ''
        self.form_name = getattr(self.form, '__form_name__', 'Form Error')

    def __unicode__(self):
        if self.form.errors:
            error_header = "<h3 class='suggestion_text'>Error in: "
            error_header += self.form_name
            error_header += "</h3>"
            self.content += error_header
            i = 1
            for k, v in self.form.errors.items():
                self.content += "<p>%s) at field name '%s' %s</span> </p>" % (
                    i, k, v)
                i += 1
        return self.content


# Form error formatter factory
def aumodelformerrorformatter_factory(form):
    form_error = AuModelFormErrorFormatter(form)
    return form_error.__unicode__()