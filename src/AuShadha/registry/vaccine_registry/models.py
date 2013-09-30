################################################################################
# PROJECT      : AuShadha
# Description  : Model for maintaining Vaccine Registry
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
################################################################################

from django.db import models
from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import AuShadhaBaseModel, AuShadhaBaseModelForm



class VaccineRegistry(AuShadhaBaseModel):

    """
      Registry for the Vaccines 
      This contains the details of vaccine, VIS,
      Manufacturer, Lot #, Expiration etc..
    """

    __model_label__ = 'vaccine_registry'

    vaccine_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    lot_number = models.CharField(max_length=100)
    manufacturing_date = models.DateField(auto_now_add=False)
    expiry_date = models.DateField(auto_now_add=False)
    vis = models.TextField("Vaccine Information Statement",
                           max_length=1000,
                           blank=True,
                           null=True
                           )

    def __unicode__(self):
        return "%s" % (self.vaccine_name)
