################################################################################
# PROJECT      : AuShadha
# Description  : {{app_name}} Models
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################


import datetime
import yaml

from django.db import models
from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel,AuShadhaBaseModelForm
from AuShadha.settings import APP_ROOT_URL
from AuShadha.apps.ui.ui import ui as UI

DEFAULT_FORM_EXCLUDES=('',)


# Put all Models and ModelForms below this