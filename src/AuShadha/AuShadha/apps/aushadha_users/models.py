##########################################################################
# Project: AuShadha Project User Models to customise Django User Model
#           and enable role and permission sharing
# License: GNU-GPL Version 3
# Author : Dr.Easwar T.R
# Date   : 03-09-2012
##########################################################################

"""
 Defining the models for AuShadha users
 
 This is a custom class to bind a logged in user to a Clinic and a Role
 
 All AuShadha uses should therefore be logged in and should have a role
 
 Fine grained permissions throughout the application can be set on role and
   permissions defined here

"""

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm


AUSHADHA_USER_ROLES = (('audhadha_admin', 'AuShadha Admin'),
                       ('aushadha_user', 'AuShadha User'),
                       ('aushadha_staff', 'AuShadha Staff '),
                       ('aushadha_developer', 'AuShadha Developer'),
                       )



class AuShadhaUser(User):

    """

     Defines AuShadhaUser class
     This is a model inheriting from User class that defines who uses AuShadha
     The user can have many roles pertaining to usage of the software. 
     This is NOT the permission on the Clinic / the Patient. 
     This is for managing / using AuShadha

    """
    aushadha_user_role = models.CharField("AuShadha User Role",
                                          help_text=""" Users Role in AuShadha Software.
                                                           This is different from the role in the Clinic""",
                                          max_length=30,
                                          choices=AUSHADHA_USER_ROLES,
                                          default="aushadha_user"
                                          )


class AuShadhaUserForm(AuthenticationForm):

    """
      Defines ModelForm for AuShadhaUser
      Generates the ModelForm for Login and authentication

    """

    model = AuShadhaUser