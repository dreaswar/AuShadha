################################################################################
# Create a Registration with the UI for a Role. 
# Each module's aushadha.py is screened for this
# 
# Each Class is registered for a Role in UI
# These can be used to generate Role based UI elements later. 
# 
# As of now string base role assignement is done. 
# This can be later extended to class based role
################################################################################

from .models import AdmissionDetail

from AuShadha.apps.ui.ui import UIClass
from AuShadha.apps.ui.ui import ui as UI

class AdmissionUI(UIClass):
    """
     Generates UI Class for Admission Object with related metadata to be passed to UI
    """

UI.register('Admission', AdmissionDetail)

