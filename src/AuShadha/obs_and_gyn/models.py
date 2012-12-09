###########################################################################################
# PROJECT: AuShadha
#          Models for managing patient Obstetric and Gynaecology history
# Author : Dr. Easwar T R
# Date   : 28-08-2012
# Licence: GNU GPL V3. Please see AuShadha/LICENSE.txt
###########################################################################################

from django.db	              import models
from django.forms	            import ModelForm
from django.core.exceptions   import ValidationError
from django 		              import forms

from aushadha_base_models.models import AuShadhaBaseModel
from clinic.models               import Clinic
from patient.models              import PatientDetail, generic_url_maker



############### Obstetric Models Start here #################

class ObstetricHistoryDetail(AuShadhaBaseModel):
  """
    Inherits from the AuShadha Base Model. 
    This defines the Obstetric History that the patient has had. 
    The patient automatically belongs to a Clinic and has some add, edit, del 
    methods defined on him. 
    
  """
  
  __model_label__  = "obstetric_history_detail"

  never_been_pregnant    = models.BooleanField('Never been pregnant', default = False)
  adoped_children        = models.BooleanField("Adopted Children ?", default = False)
  adoped_children_names  = models.TextField("Adopted Children Names", default="Not Applicable", blank = True, null = True)
  pregnancy_listing      = models.TextField(help_text='''List all pregnancies in order,including still, premature births, ectopics and abortions''',blank = True, null = True
                           )
  patient_detail         = models.ForeignKey('patient.PatientDetail',null = True,blank = True, unique = True)

  def __unicode__(self):
    return "%s" %(self.patient_detail)

  def save(self, *args, **kwargs):
    self.__model_label__ = "obstetric_history_detail"
    super(ObstetricHistoryDetail, self).save(*args, **kwargs)

  def get_edit_url(self):
      '''
      Returns the URL for editing Obstetric History details for a Patient
      '''
      return '/AuShadha/pat/%s/edit/%s/' % (self.__model_label__, self.id)

  def get_del_url(self):
      '''
      Returns the URL for editing ObstetricHistory for a Patient
      '''
      return '/AuShadha/pat/%s/del/%s/' %(self.__model_label__, self.id)


class ObstetricHistory(AuShadhaBaseModel):

  year                = models.PositiveIntegerField()
  sex                 = models.CharField(max_length = 10, 
                                         choices = (("m","Male"),
                                                    ('f',"Female"),
                                                    ("o","Others")
                                                   )
                        )
  weight              = models.DecimalField(decimal_places = 2, max_digits=4)
  type_of_delivery    = models.CharField(max_length = 50, 
                                        choices = (("normal", "Normal"),
                                                   ('cs', "Caesarian Section") 
                                                  )
                        )
  length_of_pregnancy = models.CharField(max_length = 100)
  problems            = models.TextField(max_length = 250, null = True, blank = True, default="None")
  name                = models.CharField(max_length = 100)
  age                 = models.CharField(max_length = 100)
  breast_feeding      = models.CharField("Periods of exclusive breast feeding", max_length = 100)
  obstetric_detail    = models.ForeignKey(ObstetricHistoryDetail, null= True, blank = True)

  def __unicode__(self):
    return "%s" %(self.obstetric_detail)

  def save(self, *args, **kwargs):
    self.__model_label__ = "obstetric_history"
    super(ObstetricHistory, self).save(*args, **kwargs)

  def get_edit_url(self):
      '''
      Returns the URL for editing Social details for a Patient
      '''
      return '/AuShadha/pat/%s/edit/%s/' % (self.__model_label__, self.id)

  def get_del_url(self):
      '''
      Returns the URL for adding Social for a Patient
      '''
      return '/AuShadha/pat/%s/del/%s/' %(self.__model_label__, self.id)



################## Obstetric Modelform ##################################

class ObstetricHistoryDetailForm(ModelForm):
	class Meta:
		model = ObstetricHistoryDetail
		exclude = ('patient_detail','parent_clinic')
	def __init__(self, *args, **kwargs):
		super(ObstetricHistoryDetailForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'never_been_pregnant',
		                'max_length'    :  2         ,
		                "data-dojo-type": "dijit.form.CheckBox",
		                "data-dojo-props": r"'required' :false"
		                },
                  {"field"         : 'adoped_children',
		                'max_length'    :  2         ,
		                "data-dojo-type": "dijit.form.CheckBox",
		                "data-dojo-props": r"'required' :false "
		                },
		               {"field": 'adoped_children_names',
		                'max_length'    :  100         ,
		               "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : false, disabled:true"
		               },
                    {"field"         : 'pregnancy_listing',
		                'max_length'    :  250         ,
		                "data-dojo-type": "dijit.form.Textarea",
		                "data-dojo-props": r"'required' :false, 'placeHolder': 'List all pregnancies in order including still, premature births,ectopics and abortions'"
		                }
	        ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']


class ObstetricHistoryForm(ModelForm):
	class Meta:
		model = ObstetricHistory
		exclude = ('parent_clinic', 'obstetric_detail')
	def __init__(self, *args, **kwargs):
		super(ObstetricHistoryForm, self).__init__(*args, **kwargs)
		text_fields = [{"field"         : 'year',
		                'max_length'    :  100         ,
		                "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' :true"
		                },
                  {"field"         : 'sex',
		                'max_length'    :  100         ,
		                "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' :true "
		                },
		               {"field": 'weight',
		                'max_length'    :  100         ,
		               "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : true"
		               },
                    {"field"         : 'type_of_delivery',
		                'max_length'    :  100         ,
		                "data-dojo-type": "dijit.form.Select",
		                "data-dojo-props": r"'required' :true"
		                },
                   {"field": 'length_of_pregnancy',
                   'max_length':100,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : true"
                   },
                  {"field"         : 'problems',
		                'max_length'    :  100         ,
		                "data-dojo-type": "dijit.form.Textarea",
		                "data-dojo-props": r"'required' :false"
		                },
                   {"field": 'name',
                   'max_length':100,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : true"
                   },
                  {"field"         : 'age',
		                'max_length'    :  100         ,
		                "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' :true"
		                },
                   {"field": 'breast_feeding',
                   'max_length':150,
                   "data-dojo-type": "dijit.form.ValidationTextBox",
		                "data-dojo-props": r"'required' : true"
                   }
	        ]
		for field in text_fields:
			print(self.fields[field['field']].widget);
			self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
			self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
			self.fields[field['field']].widget.attrs['max_length'] = field['max_length']



