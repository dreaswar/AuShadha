#
# Module	: AuShadha Models for Investigation & Imaging Registering
# Author	: Dr.Easwar T R
# Date		: 01-09-2012
# Licence   : GNU GPL version3 Please see AuShadha/LICENSE.txt for the License
# Notes		: Registers and Manages Investigations and Imaging.
#						Defines Model Methods, and ModelForms for the same.
#

# General Django Imports
from django.db import models
from django.forms import ModelForm


# Application specific imports
        #from patient.models 	import *
        #from admission.models import *

# Define some constants
imaging_choices = (("X-Ray"			, "X-Ray"			),
                  ("CT Scan"		, "CT Scan"		),
                  ("Ultrasound"	, "Ultrasound"),
                  ("MRI"				, "MRI"				),
                  ('Others'			, 'Others'		)
                   )


# Start Model Definitions..
class LabInvestigationRegistry(models.Model):
    name_of_investigation = models.CharField(max_length=30, unique=True)
    lower_limit = models.DecimalField(
        max_length=10, decimal_places=2, max_digits=7, default=0)
    higher_limit = models.DecimalField(
        max_length=10, decimal_places=2, max_digits=7, default=0)
    unit = models.CharField(
        max_length=20, null=True, blank=True)
    method = models.CharField(
        max_length=30, null=True, blank=True)
    analyser = models.CharField(
        max_length=30, null=True, blank=True)
    remarks = models.TextField(max_length=200,
                               default="NAD",
                               help_text='limit to 200 words'
                               )

    class Meta:
        verbose_name = 'Lab Investigation Registry'
        verbose_name_plural = 'Lab Investigation Registry'

    def __unicode__(self):
        return "%s (%s %s - %s %s)" % (self.name_of_investigation,
                                       self.lower_limit,
                                       self.unit,
                                       self.higher_limit,
                                       self.unit
                                       )

    def get_normal_range(self):
        self.range = '%s - %s' % (self.lower_limit, self.higher_limit)
        return self.range

    def abnormal_low_value(self, value):
        try:
            value = float(value)
        except(TypeError, AttributeError, NameError, ValueError):
            raise Exception(
                'Improper Value Supplied. Cannot convert to decimal. Exception!.')
        if value < float(self.lower_limit):
            return True
        else:
            return False

        def abnormal_high_value(self, value):
            try:
                value = float(value)
            except(TypeError, AttributeError, NameError, ValueError):
                raise Exception(
                    'Improper Value Supplied. Cannot convert to decimal. Exception!.')
            if value > float(self.higher_limit):
                return True
            else:
                return False


class ImagingInvestigationRegistry(models.Model):
    modality = models.CharField(max_length=30)
    area_studied = models.CharField(max_length=30)
    remarks = models.TextField(max_length=200,
                               default="NAD",
                               help_text='limit to 200 words'
                               )

    class Meta:
        verbose_name = 'Imaging Investigation Registry'
        verbose_name_plural = 'Imaging Investigation Registry'
        unique_together = ('modality', 'area_studied')

    def __unicode__(self):
        return "%s - %s" % (self.modality, self.area_studied)


# Model form definitions for Investigations..
class LabInvestigationRegistryForm(ModelForm):

    class Meta:
        model = LabInvestigationRegistry
        fields = "__all__"


class ImagingInvestigationRegistryForm(ModelForm):

    class Meta:
        model = ImagingInvestigationRegistry
        fields = "__all__"

