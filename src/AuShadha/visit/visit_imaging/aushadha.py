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

from .models import VisitDetail, VisitFollowUp, VisitComplaint, \
                    VisitHPI, VisitPastHistory, VisitROS, \
                    VisitInv, VisitImaging, VisitSOAP

from AuShadha.apps.ui.ui import ui as UI

UI.register('OPD_Visit', VisitDetail)
UI.register('OPD_Visit_Complaint', VisitComplaint)
UI.register('OPD_Visit_HPI', VisitHPI)
UI.register('OPD_Visit_PastHistory', VisitPastHistory)
UI.register('OPD_Visit_ROS', VisitROS)
UI.register('OPD_Visit_Inv', VisitInv)
UI.register('OPD_Visit_Imaging', VisitImaging)
UI.register('OPD_Visit_SOAP', VisitSOAP)
UI.register('OPD_Visit_FollowUp', VisitFollowUp)