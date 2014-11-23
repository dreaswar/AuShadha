##################################################################
# Views User Authentication and login / logout
# Author  : Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# License : GNU-GPL Version 3
# Date    : 01-01-2013
##################################################################

# Import Stdlib
import os
import sys
import urlparse
from datetime import datetime, date, time
import json

# General Django Imports

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.core.paginator import Paginator
#import json
from django.core import serializers
##from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.template.response import TemplateResponse
from django.contrib.sites.models import get_current_site



# AuShadha Imports
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.apps.aushadha_users.models import AuShadhaUser, AuShadhaUserForm




@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_view(request, template_name='registration/login.html',
               redirect_field_name=REDIRECT_FIELD_NAME,
               # authentication_form=AuthenticationForm,
               authentication_form=AuShadhaUserForm,
               current_app=None, extra_context=None):
    """Displays the login form and handles the login action."""
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            data = {'success': True,
                    'error_message': "Successfully Loggged In !",
                    'redirect_to': redirect_to
                    }
        else:
            data = {'success': False,
                    'error_message' : '''<em class='error_text'>ERROR! Could not login</em>
                                         <p class='suggestion_text'>Please Check your Username & Password.</p>
                                         <i class='help_text'>If you are sure they are correct, 
                                         Please contact Administrator to find 
                                         out whether you need to activate your account.
                                         </i>
                                       ''',
                    }
        jsondata = json.dumps(data)
        return HttpResponse(jsondata, content_type='application/json')
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@login_required
def logout_view(request):
    """View for logging out of AuShadha."""
    logout(request)
    #return HttpResponseRedirect('/AuShadha/')
    return HttpResponseRedirect('/login/')
# Create your views here.
