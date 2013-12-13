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

from .models import AdmissionDetail, AdmissionComplaint, AdmissionHPI, \
                    AdmissionPastHistory, AdmissionROS, AdmissionInv, AdmissionImaging

from AuShadha.apps.ui.ui import ui as UI

UI.register('Admission', AdmissionDetail)

UI.register('Admission_Complaint', AdmissionComplaint)
UI.register('Admission_HPI', AdmissionHPI)
UI.register('Admission_PastHistory', AdmissionPastHistory)
UI.register('Admission_ROS', AdmissionROS)
UI.register('Admission_Inv', AdmissionInv)
UI.register('Admission_Imaging', AdmissionImaging)
