VITAL_FORM_CONSTANTS = {

                        'sys_bp': {'max_length': 100,
                                   "data-dojo-type": "dijit.form.NumberSpinner",
                                   "data-dojo-props": r"'required' :true,placeHolder:'mmHg',smallDelta:2, constraints:{min:0,max:300,places:0}",
                                   'style': r'width:100px;'
                        },

                        'dia_bp': {'max_length': 100,
                                   "data-dojo-type": "dijit.form.NumberSpinner",
                                   "data-dojo-props": r"'required' :true,placeHolder:'mmHg',smallDelta:2, constraints:{min:0,max:200,places:0}",
                                   'style': r'width:100px;'
                        },

                        'pulse_rate': {'max_length': 100,
                                       "data-dojo-type": "dijit.form.NumberSpinner",
                                       "data-dojo-props": r"'required' : false,placeHolder:'per min',smallDelta:2, constraints:{min:0,max:250,places:0}",
                                       'style': r'width:100px;'
                        },

                        'resp_rate': {'max_length': 100,
                                      "data-dojo-type": "dijit.form.NumberSpinner",
                                      "data-dojo-props": r"'required' :false,placeHolder:'per minute',smallDelta:2, constraints:{min:0,max:100,places:0}",
                                      'style': r'width:100px;'
                        },

                        'gcs': {'max_length': 100,
                                "data-dojo-type": "dijit.form.NumberSpinner",
                                "data-dojo-props": r"'required' : false,placeHolder:'out of 15',smallDelta:1, constraints:{min:0,max:15,places:0}",
                                'style': r'width:100px;'
                        },

                        'height': {'max_length': 100,
                                   "data-dojo-type": "dijit.form.NumberSpinner",
                                   "data-dojo-props": r"'required' :false, placeHolder:'in cms',smallDelta:1, constraints:{min:0,max:250,places:2}",
                                   'style': r'width:100px;'
                        },

                        'weight': {
                            'max_length': 100,
                            "data-dojo-type": "dijit.form.NumberSpinner",
                            "data-dojo-props": r"'required' :false,placeHolder:'in Kgs',smallDelta:1, constraints:{min:0,max:200,places:2}",
                            'style': r'width:100px;'
                        },

                        'bmi': {'max_length': 100,
                                "data-dojo-type": "dijit.form.NumberSpinner",
                                "data-dojo-props": r"'required' : true,smallDelta:0.5, constraints:{min:0,max:50,places:2}",
                                'style': r'width:100px;'
                        },

                        'temp': {'max_length': 100,
                                "data-dojo-type": "dijit.form.NumberSpinner",
                                "data-dojo-props": r"'required' : true,smallDelta:0.5, constraints:{min:0,max:50,places:2}",
                                'style': r'width:100px;'
                        }

                    }

GEN_EXAM_FORM_CONSTANTS = {
                        'pallor': {
                            'max_length': 100,
                            "data-dojo-type": "dijit.form.CheckBox",
                            "data-dojo-props": r"'required' :false"
                        },
                        'icterus': {
                            'max_length': 100,
                            "data-dojo-type": "dijit.form.CheckBox",
                            "data-dojo-props": r"'required' :false"
                        },
                        'cyanosis': {
                            'max_length': 100,
                            "data-dojo-type": "dijit.form.CheckBox",
                            "data-dojo-props": r"'required' : false"
                        },
                        'clubbing': {
                            'max_length': 100,
                            "data-dojo-type": "dijit.form.CheckBox",
                            "data-dojo-props": r"'required' :false"
                        },
                        'lymphadenopathy': {
                            'max_length': 100,
                            "data-dojo-type": "dijit.form.CheckBox",
                            "data-dojo-props": r"'required' : false"
                        },
                        'edema': {
                            'max_length': 100,
                            "data-dojo-type": "dijit.form.CheckBox",
                            "data-dojo-props": r"'required' :false"
                        }
}

PHY_EXAM_BASE_MODEL_FORM_CONSTANTS = {
    'base_model': {'max_length': 100,
              "data-dojo-type": "dijit.form.ValidationTextBox",
              "data-dojo-props": r"'required' :false"
              }
}

SYS_EXAM_FORM_CONSTANTS = {
    'heent': {'max_length': 1000,
              "data-dojo-type": "dijit.form.Textarea",
              "data-dojo-props": r"'required' :false"
              },
    'cns': {'max_length': 1000,
            "data-dojo-type": "dijit.form.Textarea",
            "data-dojo-props": r"'required' :false"
            },
    'cvs': {'max_length': 1000,
            "data-dojo-type": "dijit.form.Textarea",
            "data-dojo-props": r"'required' : false"
            },
    'respiratory_system': {'max_length': 1000,
                           "data-dojo-type": "dijit.form.Textarea",
                           "data-dojo-props": r"'required' :false"
                           },
    'git_and_gut': {'max_length': 1000,
                    "data-dojo-type": "dijit.form.Textarea",
                    "data-dojo-props": r"'required' : false"
                    }
}


MUSCULOSKELETAL_EXAM_FORM_CONSTANTS = {
    'ms_exam': {
        'max_length': 3000,
        "data-dojo-type": "dijit.Editor",
        "data-dojo-props": r"'required' :true",
        'class': r"ms_exam_textarea"
    }
}


NEURO_EXAM_FORM_CONSTANTS = {
    'plantar': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' :false"
    },
    'abdominal': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' :false"
    },
    'cremasteric': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' : false"
    },
    'anal_wink': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' :false"
    },
    'motor': {
        'max_length': 250,
        "data-dojo-type": "dijit.form.Textarea",
                          "data-dojo-props": r"'required' : false"
    },
    'sensory': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' : false"
    },
    'dtr': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' : false"
    },
    'cranial_nerve': {
        'max_length': 250,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' : false"
    }
}

VASCULAR_EXAM_FORM_CONSTANTS = {
    'location': {
        'max_length': 30,
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' :false"
    },
    'side': {'max_length': 30,
             "data-dojo-type": "dijit.form.Select",
                               "data-dojo-props": r"'required' :false"
             },
    'character': {'max_length': 30,
                  "data-dojo-type": "dijit.form.Select",
                  "data-dojo-props": r"'required' : false"
                  }

}
