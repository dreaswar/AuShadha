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

NEURO_EXAM={
    'plantar': "Bilateral Flexor response",

    'abdominal':"Ellicited well in all four quadrants",

    "cremasteric":"Present",

    "anal_wink":"Present",

    "motor": "Normal Bulk, Tone and Power in all four limbs. No Fasciculations",

    "sensory": "Normal Sensation in all four limbs. Perianal sensation intact",

    "dtr" : "Equally ellicitable in all four limbs. No Clonus",

    "cranial_nerve" :"All Cranial Nerves NAD"
    }

MUSCULOSKELETAL_EXAM = {
    "ms_exam": "NAD"
}

CONSULT_CHOICES = (
    ('initial', 'Initial'       ),
    ('fu', 'Follow-Up'),
    ('pre_op', 'Pre-Op'),
    ('post_op', 'Post-OP'),
    ('discharge', 'Discharge')
)


PC = {

   'visit_ros': {
      'const_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Constitutional Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'eye_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Eye Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'ent_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'ENT Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'cvs_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Cardiovascular Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'resp_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Respiratory Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'gi_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Gastro-Intestinal Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'gu_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Genitourinary Symptoms',
                      'unit'     :'',
                      'delimitter':''
                   },
      'integ_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Integumentary /Breast Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'neuro_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Neurological Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'psych_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Psychiatric Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'endocr_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Endocrine Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'hemat_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Hematological Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    },
      'immuno_symp': {'default':"Nil",
                      'constraints':{},
                      'validator':'is_not_equal_to',
                      'label' :'Immunologic Symptoms',
                      'unit'     :'',
                      'delimitter':''
                    }
   },

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
                     'delimitter':''
                     },
            'temp': {'default':98.40,
                     'constraints':{'max':120.0,'min':90.00},
                     'validator':'is_in_range',
                      'label' :'Temparature',                     
                     'unit'     :'Farenheit',
                     'delimitter':' '
                     },
            'remarks': {'default':"NAD",
                       'constraints':{},
                       'validator':'is_not_equal_to',
                       'label' :'Remarks',                       
                       'unit'     :' ',
                       'delimitter':':'
                       }
            },

   'gen':{'pallor':{'default':False,
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
                       'validator':'is_not_equal_to',
                       'label' :'Remarks',                       
                       'unit'     :' ',
                       'delimitter':''
                       }
              },

  'sys':{        
              'heent': {'default':HEENT_EX,
                        'constraints':{},
                        'validator':'is_not_equal_to',
                        'label' :'HEENT Examination',                       
                        'unit'     :' ',
                        'delimitter':''
                        },

              'cns': {'default':CNS_EX,
                        'constraints':{},
                        'validator':'is_not_equal_to',
                        'label' :'Central Nervous Examination',                       
                        'unit'     :' ',
                        'delimitter':''
                        },
              
              'cvs': {'default':CVS_EX,
                        'constraints':{},
                        'validator':'is_not_equal_to',
                        'label' :'Cardio-Vascular Examination',                       
                        'unit'     :' ',
                        'delimitter':''
                        },

              'respiratory_system': {'default':RESP_EX,
                                      'constraints':{},
                                      'validator':'is_not_equal_to',
                                      'label' :'Respiratory System Examination',                       
                                      'unit'     :' ',
                                      'delimitter':''
                                      },

               'git_and_gut': {'default':GIT_GUT_EX,
                              'constraints':{},
                              'validator':'is_not_equal_to',
                              'label' :'GastroIntestinal & Genitourinary System Examination',                       
                              'unit'     :' ',
                              'delimitter':''
                              },

                },

   'neuro':{
                    'plantar': {'default':NEURO_EXAM['plantar'],
                                'constraints':{},
                                'validator':'is_not_equal_to',
                                'label' :'Plantar Reflex',                       
                                'unit'     :' ',
                                'delimitter':''
                                },

                    'cremasteric': {'default':NEURO_EXAM['cremasteric'],
                                    'constraints':{},
                                    'validator':'is_not_equal_to',
                                    'label' :'Cremasteric Reflex',                       
                                    'unit'     :' ',
                                    'delimitter':''
                                    },

                    'abdominal': {'default':NEURO_EXAM['abdominal'],
                                  'constraints':{},
                                  'validator':'is_not_equal_to',
                                  'label' :'Abdominal Reflexes',                       
                                  'unit'     :' ',
                                  'delimitter':''
                                  },

                    'anal_wink': {'default':NEURO_EXAM['anal_wink'],
                                  'constraints':{},
                                  'validator':'is_not_equal_to',
                                  'label' :'Anal Wink',                       
                                  'unit'     :' ',
                                  'delimitter':''
                                  },

                    'motor': {'default':NEURO_EXAM['motor'],
                              'constraints':{},
                              'validator':'is_not_equal_to',
                              'label' :'Motor Examination',                       
                              'unit'     :' ',
                              'delimitter':''
                              },

                    'sensory': {'default':NEURO_EXAM['sensory'],
                                'constraints':{},
                                'validator':'is_not_equal_to',
                                'label' :'Sensory Examination',                       
                                'unit'     :' ',
                                'delimitter':''
                                },

                    'dtr': {'default':NEURO_EXAM['dtr'],
                            'constraints':{},
                            'validator':'is_not_equal_to',
                            'label' :'Deep Reflexes',                       
                            'unit'     :' ',
                            'delimitter':''
                            },

                    'cranial_nerve': {'default':NEURO_EXAM['cranial_nerve'],
                                      'constraints':{},
                                      'validator':'is_not_equal_to',
                                      'label' :'Cranial Nerve',                       
                                      'unit'     :' ',
                                      'delimitter':''
                                      }

     },

   'musculoskeletal':{

                'ms_exam': {'default':MUSCULOSKELETAL_EXAM['ms_exam'],
                            'constraints':{},
                            'validator':'is_not_equal_to',
                            'label' :'Findings',
                            'unit'     :' ',
                            'delimitter':''
                            }

    },

   'vasc':{
                    'location': {'default':['DP','PT','P','F','R','U','B','A','SC','C'],
                                'constraints':{},
                                'validator':'in_list',
                                'label' :'Location',                       
                                'unit'     :' ',
                                'delimitter':''
                                },

                    'side': {'default':['R','L','B'],
                            'constraints':{},
                            'validator':'in_list',
                            'label' :'Side',                       
                            'unit'     :' ',
                            'delimitter':''
                            },

                    'character': {'default':'normal',
                                  'constraints':{},
                                  'validator':'is_not_equal_to',
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