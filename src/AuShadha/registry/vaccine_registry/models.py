##########################################################################
# PROJECT      : AuShadha
# Description  : Model for maintaining Vaccine Registry
# Author       : Dr. Easwar T R
# Date         : 16-09-2013
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
##########################################################################

from django.db import models
from django.contrib.auth.models import User

from AuShadha.apps.aushadha_base_models.models import (
    AuShadhaBaseModel,
    AuShadhaBaseModelForm
)


class VaccineDetail(AuShadhaBaseModel):
    """
      Vaccine Detail Class derived from CVX XML from CDC

      **vaccine_id** :
           - is unique. It is otherwise called the CVX Code by CDC
      **pk**
           - has been set to tbe same as vaccine_id has been set via fixtures
           - so VaccineDetail.objects.get(pk = vaccine_id) would be valid
    """

    __model_label__ = 'vaccine_detail'

    vaccine_id = models.PositiveIntegerField(max_length=30, unique=True)

    def __unicode__(self):
        """ returns the unicode """
        return "%s (%s)" % (self.get_vaccine_name(), self.vaccine_id)

    def get_vaccine_name(self):
        """ returns the vaccine name """
        if self.vaccine_id:
            v_id = int(self.vaccine_id)
            v_obj = VaccineDetail.objects.get(pk=v_id)
            v_data = VaccineData.objects.filter(
                vaccine_fk=v_obj).filter(
                field_name="ShortDescription")
            if v_data:
                return "%s" % (v_data[0].field_value)
        return ''


class VaccineData(AuShadhaBaseModel):
    """ Vaccine Data from CVX of CDC """

    __model_label__ = 'vaccine_data'

    field_name = models.CharField(max_length=30)
    field_value = models.TextField(max_length=1000, null=True, blank=True)
    vaccine_fk = models.ForeignKey('VaccineDetail')

    def __unicode__(self):
        """ unicode representation """
        return "%s : %s" % (self.field_name, self.field_value)


class VaccineCVXToMVX(AuShadhaBaseModel):

    """
    SCHEMA:
      "Short Description": "vaccinia (smallpox)",
      "CVXCode": "75        ",
      "MVX Code": "PMC       ",
      "Last Updated": "5/28/2010",
      "Product name Status": "Active",
      "MVX Status": "Active",
      "CDC Product Name": "ACAM2000",
      "Manufacturer": "sanofi pasteur"
    """

    __model_label__ = 'vaccine_cvx_to_mvx'

    short_description = models.TextField(max_length=500)
    cvxcode = models.ForeignKey('VaccineDetail')
    mvx_code = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=False,
                                        auto_now_add=False,
                                        null=True,
                                        blank=True)
    product_name_status = models.CharField(max_length=50,
                                           choices=(('active', 'Active',),
                                                    ('inactive', 'Inactive')
                                                    ),
                                           null=True, blank=True
                                           )
    mvx_status = models.CharField(max_length=50,
                                  choices=(('active', 'Active',),
                                           ('inactive', 'Inactive')
                                           ),
                                  null=True, blank=True)
    cdc_product_name = models.TextField(max_length=100, null=True, blank=True)
    manufacturer = models.TextField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return "%s %s (%s)" % (self.short_description,
                               self.cvx_code, self.manufacturer)


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
