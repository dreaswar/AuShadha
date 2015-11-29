from django.db import models

#############################################
# Author   : Dr. Easwar T R
# Date         : 12-10.2015
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
#############################################

from django.db import models
from django.contrib.auth.models import User

from AuShadha.settings import APP_ROOT_URL
from AuShadha.utilities.urls import generic_url_maker
from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel,\
    AuShadhaBaseModelForm
from AuShadha.apps.clinic.models import Clinic

from dijit_fields_constants import SIMPLENOTES_FIRST_VISIT_FORM_CONSTANTS
SIMPLENOTES_FIRST_VISIT_FORM_EXCLUDES = ('visit_detail',)

from visit.visit.models import VisitDetail


class SimpleNotes_FirstVisit(AuShadhaBaseModel):

    """
    First Visit notes
    """

    def __init__(self, *args, **kwargs):
        super(SimpleNotes_FirstVisit, self).__init__(*args, **kwargs)
        self.__model_label__ = "simplenotes_first_visit"
        self._parent_model = 'visit_detail'
        self._can_add_list_or_json = []
        self._extra_url_actions = []

    # Model attributes
    complaints = models.TextField(max_length=300)
    history_of_present_illness = models.TextField(max_length=1000,
                                                  blank=True,
                                                  null=True)
    past_history = models.TextField(max_length=500,
                                    blank=True,
                                    null=True,
                                    )
    treatment_history = models.TextField(max_length=500,
                                         null=True,
                                         blank=True
                                         )
    birth_history = models.TextField(max_length=500,
                                     null=True,
                                     blank=True
                                     )

    family_history = models.TextField(max_length=500, blank=True, null=True)
    personal_history = models.TextField(max_length=500, null=True, blank=True)
    regional_examination = models.TextField(max_length=500)
    systemic_examination = models.TextField(max_length=500, default="NAD")
    vitals = models.TextField(max_length=250, null=True, blank=True)
    investigation_notes = models.TextField(
        max_length=500, null=True, blank=True)
    summary = models.TextField(max_length=500)
    diagnosis = models.TextField(max_length=500)
    plan = models.TextField(max_length=500)
    visit_detail = models.ForeignKey(VisitDetail)

    class Meta:
        verbose_name = "Simple Visit Notes- First Visit"
        verbose_name_plural = "Simple Visit Notes- First Visit"
        ordering = ('complaints',
                    'history_of_present_illness',
                    'past_history',
                    'treatment_history',
                    'birth_history',
                    'family_history',
                    'personal_history',
                    'regional_examination',
                    'systemic_examination',
                    'vitals',
                    'investigation_notes',
                    'summary',
                    'diagnosis',
                    'plan',
                    )

    def __unicode__(self):
        pass

    def save(self, *args, **kwargs):
        pass


class SimpleNotesFirstVisitForm(AuShadhaBaseModelForm):

    """
        ModelForm for Simple Notes First Visit
    """

    __form_name__ = "Visit Notes -First Visit"

    dijit_fields = SIMPLENOTES_FIRST_VISIT_FORM_CONSTANTS

    class Meta:
        model = SimpleNotes_FirstVisit
        exclude = SIMPLENOTES_FIRST_VISIT_FORM_EXCLUDES
