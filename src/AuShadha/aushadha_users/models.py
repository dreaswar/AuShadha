#
# Project: AuShadha Project User Models to customise Django User Model
#           and enable role and permission sharing
# License: GNU-GPL Version 3
# Author : Dr.Easwar T.R
# Date   : 03-09-2012
#

from django.db import models
from django.forms import ModelForm


#from patient.models   import PatientDetail
#from clinic.models    import Clinic
#from physician.models import *
#from nurses.models    import *
#from staff.models     import *

from django.contrib.auth.models import User
#from django.contrib.auth.views       import login, logout
#from django.contrib.auth.decorators  import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm


AUSHADHA_USER_ROLES = (('audhadha_admin', 'AuShadha Admin'),
                       ('aushadha_user', 'AuShadha User'),
                       ('aushadha_staff', 'AuShadha Staff '),
                       ('aushadha_developer', 'AuShadha Developer'),
                       )


# Defining the models for AuShadha users
# This is a custom class to bind a logged in user to a Clinic and a Role
# All AuShadha uses should therefore be logged in and should have a role
# Fine grained permissions throughout the application can be set on role and
# permissions defined here
class AuShadhaUser(User):
    aushadha_user_role = models.CharField("AuShadha User Role",
                                          help_text=""" Users Role in AuShadha Software.
                                                           This is different from the role in the Clinic""",
                                          max_length=30,
                                          choices=AUSHADHA_USER_ROLES,
                                          default="aushadha_user"
                                          )


class AuShadhaUserForm(AuthenticationForm):
    model = AuShadhaUser
