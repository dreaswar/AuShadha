################################################################################
# Physical Examination and Validation Constants for AuShadha.
# These Provide Default constants
################################################################################
# Author    : Dr.Easwar T.R
# Copyright : 2012
# Date      : 2013-09-07
# Licence   : GNU-GPL Version 3
################################################################################


# PHYSICAL EXAMINATION CONSTANTS FOR VALIDATION IN PRESENTATION CLASSES

class Validator(object):
  """
  Validates a field for values
  """
  accepted_methods = ['is_in_range',
                      'is_greater',
                      'is_lesser',
                      'is_later',
                      'is_in_between',
                      'is_earlier',
                      'is_true_or_false',
                      'is_equal_to',
                      'contains_text',
                      None
                     ]

  def __init__(self, 
               method,
               value_to_validate, 
               constraints = None,
               value_to_compare=None):

    if method in self.accepted_methods:
      self.method_map = {'is_in_range':self.is_in_range,
                        'is_greater':self.is_greater,
                        'is_lesser':self.is_lesser,
                        'is_later':self.is_later,
                        'is_in_between':None,
                        'is_earlier':self.is_earlier,
                        'is_true_or_false':self.is_true_or_false,
                        'is_equal_to':self.is_equal_to,
                        'contains_text':None,
                        None:None
                        }
      self.method_to_call = self.method_map[method]
      self.constraints = constraints
      self.value_to_validate = value_to_validate
      self.value_to_compare = value_to_compare
    else:
      print "ERROR! You have asked for validation with ", method
      raise Exception("Invalid Method. Not in accepted validator list")

  def __call__(self):
    attr = getattr(self,'method_to_call',None)
    return attr()

  def is_in_range(self):
    max_v = self.constraints['max']+1
    if self.value_to_validate in range( self.constraints['min'], max_v ):
      print "Value is in range"
      return True
    else:
      print "Value not in range"
      return False

  def is_equal_to(self):
    if self.value_to_validate == self.value_to_compare:
      return True
    else:
      return False

  def is_greater(self):
    if self.value_to_validate > self.value_to_compare:
      return True
    else:
      return False

  def is_lesser(self):
    if self.value_to_validate < self.value_to_compare:
      return True
    else:
      return False

  def is_earlier(self):
    if value_to_validate <value_to_compare:
      return True
    else:
      return False

  def is_later(self):
    if self.value > self.value_to_compare:
      return True
    else:
      return False

  def is_true_or_false(self,v):
    if self.value_to_validate == True:
      return True
    else:
      return False


def validator_factory(method,value,constraints=None,value_to_compare = None):
  """ Returns a instantiated Validator Class """
  return Validator(method,value,constraints,value_to_compare)













# PHYSICAL EXAMINATION AND INCIDENT CONSTANTS
EXAMINATION_SIDES = (('R', "Right"), ("L", "Left"), ("B/L", "Bilateral"))

INCIDENT_TYPES = (
    ('drug_related', "Drug Related"),
    ("procedure_related",
     "Procedure Related"        ),
    ("anaesthesia_related",
     "Anaesthesia Related"  ),
    ("others", "Others"),
)

# SYS EXAM NORMALS
HEENT_EX = "No abnormality detected in Head/ Eye/ Ear/ Nose/ Throat and Neck Exam"

CNS_EX         = """
Higher functions normal. GCS 15/ 15.\n
No cranial nerve palsy.\n
No Motor or Sensory Deficit.\n
Deep and Superficial reflexes normal.\n
"""

CVS_EX         = """
Heart sounds normal.\n
Carotid pulsations well felt on both sides.\n
Peripheral pulses well felt on all four limbs.\n
"""

RESP_EX        = """
Air entry equal on both sides.\n
No abnormal breath sounds.\n
Normal Percussion findings. \n
No tenderness in chest wall.\n
"""

GIT_GUT_EX     = """
Abdomen soft and non-tender in all four quadrants.\n
No organomegaly.\n
No abnormal mass palpable.\n
No free fluid or dilated veins.\n
No renal angle tenderness or impulse on cough.\n
No abnormal findings in External genitalia\n
No Inguinal Lymphadenopathy.\n
"""


# REGIONAL EXAM NORMALS
NORM_LIMB_INS  = """
Attitude of limbs normal on both sides.\n
No wasting or apparent Limb length inequality observed.\n
No Apparent deformity, swelling, wounds or discharge noted.\n
"""

NORM_LIMB_PALP = """
No joint line or spinal tenderness, swelling or local warmth noted.\n
No spasm on attempted movements.\n
No abnormal joint laxity or deformity noted.\n
ASIS and shoulders at the same level.\n
Spine profile WNL. No Scoliosis or other deformity noted clinically.\n
No apparent / true limb length inequality.\n
Limb alignment normal.\n
"""

NORM_GAIT      = """
Gait unassisted and stable.\n
No limp / lurch.\n
Trendlenberg test negative.\n
"""

NORM_ROM       = """
Full range of movements of all joints and spine.No fixed deformity.\n
No Pain, spasm / crepitus on movements.\n
No soft tissue contracture.\n
"""

CONSULT_CHOICES = (
    ('initial', 'Initial'       ),
    ('fu', 'Follow-Up'),
    ('pre_op', 'Pre-Op'),
    ('post_op', 'Post-OP'),
    ('discharge', 'Discharge')
)


PC = {

   'vital':{'sys_bp': {'default':120,
                       'constraints':{'max':150,'min':90},
                       'validator':'is_in_range',
                       'label' :'Systolic BP',
                       'unit'     :'mmHg',
                       'delimitter':'/'
                       },
            'dia_bp': {'default':80,
                       'constraints':{'max':90,'min':70},
                       'validator':'is_in_range',
                       'label' :'Diastolic BP',                       
                       'unit'     :'mmHg',
                       'delimitter':'/'
                       },
            'pulse_rate': {'default':80,
                        'constraints':{'max':100,'min':70},
                         'validator':'is_in_range',
                       'label' :'Pulse Rate',                         
                         'unit'     :'per min.',
                         'delimitter':' '
                       },
            'resp_rate': {'default':20,
                         'constraints':{'max':28,'min':18},
                         'validator':'is_in_range',
                       'label' :'Respiratory Rate',                         
                         'unit'     :'per min.',
                         'delimitter':':'
                       },
            'gcs': {'default':15,
                    'constraints':{'max':15,'min':15},
                    'validator':'is_in_range',
                       'label' :'GCS',                    
                    'unit'     :'15',
                    'delimitter':'/'
                    },
            'height': {'default':0,
                       'constraints':{},
                       'validator':None,
                       'label' :'Height',                       
                       'unit'     :'Cms.',
                       'delimitter':':'
                       },
            'weight': {'default':0,
                       'constraints':{},
                       'validator':None,
                       'label' :'Weight',                       
                       'unit'     :'Kg.',
                       'delimitter':':'
                       },
            'bmi': {'default':25.00,
                     'constraints':{'max':28.00,'min':22.00},
                     'validator':'is_in_range',
                       'label' :'BMI',                     
                     'unit'     :' ',
                     'delimitter':':'
                     },
            'remarks': {'default':"NAD",
                       'constraints':{},
                       'validator':'is_equal_to',
                       'label' :'Remarks',                       
                       'unit'     :' ',
                       'delimitter':':'
                       }
            },

   'gen_exam':{'pallor':{'default':False,
                       'constraints':{},
                       'validator':'is_true_or_false',
                       'label' :'Pallor',                       
                       'unit'     :' ',
                       'delimitter':':'
                       },
              'icterus': {'default':False,
                       'constraints':{},
                       'validator':'is_true_or_false',
                       'label' :'Icterus',                       
                       'unit'     :' ',
                       'delimitter':':'
                       },
              'cyanosis': {'default':False,
                       'constraints':{},
                       'validator':'is_true_or_false',
                       'label' :'Cyanosis',                       
                       'unit'     :' ',
                       'delimitter':':'
                       },
              'lymphadenopathy': {'default':False,
                       'constraints':{},
                       'validator':'is_true_or_false',
                       'label' :'Lymphadenopathy',                       
                       'unit'     :' ',
                       'delimitter':':'
                       },
              'clubbing': {'default':False,
                       'constraints':{},
                       'validator':'is_true_or_false',
                       'label' :'Clubbing',                       
                       'unit'     :' ',
                       'delimitter':':'
                       },
              'edema': {'default':False,
                       'constraints':{},
                       'validator':'is_true_or_false',
                       'label' :'Edema',                       
                       'unit'     :' ',
                       'delimitter':':'
                       },
              'remarks': {'default':"NAD",
                       'constraints':{},
                       'validator':'is_equal_to',
                       'label' :'Remarks',                       
                       'unit'     :' ',
                       'delimitter':''
                       }
              },

  'sys_exam':{        
              'heent': {'default':HEENT_EX,
                        'constraints':{},
                        'validator':'is_equal_to',
                        'label' :'HEENT Examination',                       
                        'unit'     :' ',
                        'delimitter':''
                        },

              'cns': {'default':CNS_EX,
                        'constraints':{},
                        'validator':'is_equal_to',
                        'label' :'Central Nervous Examination',                       
                        'unit'     :' ',
                        'delimitter':''
                        },
              
              'cvs': {'default':CVS_EX,
                        'constraints':{},
                        'validator':'is_equal_to',
                        'label' :'Cardio-Vascular Examination',                       
                        'unit'     :' ',
                        'delimitter':''
                        },

              'respiratory_system': {'default':RESP_EX,
                                      'constraints':{},
                                      'validator':'is_equal_to',
                                      'label' :'Respiratory System Examination',                       
                                      'unit'     :' ',
                                      'delimitter':''
                                      },

               'git_and_gut': {'default':GIT_GUT_EX,
                              'constraints':{},
                              'validator':'is_equal_to',
                              'label' :'GastroIntestinal & Genitourinary System Examination',                       
                              'unit'     :' ',
                              'delimitter':''
                              },

                },

   'neuro_exam':{
                    'plantar': {'default':'',
                                'constraints':{},
                                'validator':'is_equal_to',
                                'label' :'Plantar Reflex',                       
                                'unit'     :' ',
                                'delimitter':''
                                },

                    'cremasteric': {'default':'',
                                    'constraints':{},
                                    'validator':'is_equal_to',
                                    'label' :'Cremasteric Reflex',                       
                                    'unit'     :' ',
                                    'delimitter':''
                                    },

                    'abdominal': {'default':'',
                                  'constraints':{},
                                  'validator':'is_equal_to',
                                  'label' :'Abdominal Reflexes',                       
                                  'unit'     :' ',
                                  'delimitter':''
                                  },

                    'anal_wink': {'default':'',
                                  'constraints':{},
                                  'validator':'is_equal_to',
                                  'label' :'Anal Wink',                       
                                  'unit'     :' ',
                                  'delimitter':''
                                  },

                    'motor': {'default':'',
                              'constraints':{},
                              'validator':'is_equal_to',
                              'label' :'Motor Examination',                       
                              'unit'     :' ',
                              'delimitter':''
                              },

                    'sensory': {'default':'',
                                'constraints':{},
                                'validator':'is_equal_to',
                                'label' :'Sensory Examination',                       
                                'unit'     :' ',
                                'delimitter':''
                                },

                    'dtr': {'default':'',
                            'constraints':{},
                            'validator':'is_equal_to',
                            'label' :'Deep Reflexes',                       
                            'unit'     :' ',
                            'delimitter':''
                            },

                    'cranial_nerve': {'default':'',
                                      'constraints':{},
                                      'validator':'is_equal_to',
                                      'label' :'Cranial Nerve',                       
                                      'unit'     :' ',
                                      'delimitter':''
                                      },

     },

   'vascular_exam':{
                    'location': {'default':'',
                                'constraints':{},
                                'validator':'is_equal_to',
                                'label' :'Location',                       
                                'unit'     :' ',
                                'delimitter':''
                                },

                    'side': {'default':'',
                            'constraints':{},
                            'validator':'is_equal_to',
                            'label' :'Side',                       
                            'unit'     :' ',
                            'delimitter':''
                            },

                    'character': {'default':'Normal',
                                  'constraints':{},
                                  'validator':'is_equal_to',
                                  'label' :'Character',                       
                                  'unit'     :' ',
                                  'delimitter':''
                                  },

     },

   'obstetric_exam':{},

   'gynaecological_exam':{},

   'neonatal_exam':{},

   'paediatric_exam':{},

   'cardiac_exam':{},

   'musculoskeletal_exam':{},
  }