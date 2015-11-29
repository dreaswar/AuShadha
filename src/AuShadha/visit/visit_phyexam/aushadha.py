##########################################################################
# Create a Registration with the UI for a Role.
# Each module's aushadha.py is screened for this
#
# Each Class is registered for a Role in UI
# These can be used to generate Role based UI elements later.
#
# As of now string base role assignement is done.
# This can be later extended to class based role
##########################################################################

from .models import PhyExamBaseModel, VitalExam, GenExam, SysExam, NeuroExam, VascExam, MusculoSkeletalExam
from AuShadha.apps.ui.ui import ui as UI

UI.register('OPD_Visit_PhysicalExamination', PhyExamBaseModel)
UI.register('OPD_Visit_VitalExam', VitalExam)
UI.register('OPD_Visit_GenExam', GenExam)
UI.register('OPD_Visit_SysExam', SysExam)
UI.register('OPD_Visit_MusculoSkeletalExam', MusculoSkeletalExam)
UI.register('OPD_Visit_NeuroExam', NeuroExam)
UI.register('OPD_Visit_VascExam', VascExam)
