VISIT_DETAIL_FORM_CONSTANTS = {
  'visit_date':{
                'max_length': 100,
                "data-dojo-type": "dijit.form.DateTextBox",
                "data-dojo-props": r"'required' :true"
  },
  'op_surgeon':{
                'max_length': 100,
                "data-dojo-type": "dijit.form.Select",
                "data-dojo-props": r"'required' : true"
  },
  'referring_doctor':{
                'max_length': 100,
                "data-dojo-type": "dijit.form.ValidationTextBox",
                "data-dojo-props": r"'required' :false"
  },
  'consult_nature':{
                'max_length': 100,
                "data-dojo-type": "dijit.form.Select",
                "data-dojo-props": r"'required' :true"
  },
  'status':{
              'max_length': 100,
              "data-dojo-type": "dijit.form.Select",
              "data-dojo-props": r"'required' :true"
  },
  'remarks':{
              'max_length': 150,
              "data-dojo-type": "dijit.form.Textarea",
              "data-dojo-props": r"'required' :false"
  }
}
  
VISIT_COMPLAINTS_FORM_CONSTANTS = {

            #{"field"           : 'visit_detail',
            #'max_length'     :  '100'         ,
            #"data-dojo-type" : "dijit.form.Select",
            # "data-dojo-props": r"'required' : false ,'readOnly':true,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'",
            #'style':r"display:none;"
            #},
            #{"field"           : 'parent_clinic',
            #'max_length'     :  '100'         ,
            #"data-dojo-type" : "dijit.form.Select",
            # "data-dojo-props": r"'required' : false ,'readOnly':true,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'",
            #'style':r"display:none;"
            #},
            #{"field"           : 'base_model',
            #'max_length'     :  '100'         ,
            #"data-dojo-type" : "dijit.form.ValidationTextBox",
            # "data-dojo-props": r"'required' : false ,'readOnly':true,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'",
            #'style':r"display:none;"
            #},
          'complaint':{
                    'max_length': '100',
                    "data-dojo-type": "dijit.form.ValidationTextBox",
                    "data-dojo-props": r"'required' : false ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'",
          },
          'duration':{
                    'max_length': '100',
                    "data-dojo-type": "dijit.form.ValidationTextBox",
                    "data-dojo-props": r"'required' : false ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'",
          }  
}

VISIT_HPI_FORM_CONSTANTS = {
            'hpi':{
                'max_length': '1000',
                "data-dojo-type": "dijit/form/SimpleTextarea",
                "data-dojo-id": "visit_hpi",
                "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-_:0-9#]+','invalidMessage' : 'Invalid Character'",
                "style" : r"width: 70%;min-width:50%;"
             }  
}

VISIT_PAST_HISTORY_FORM_CONSTANTS = {
            'past_history':{
                'max_length': '1000',
                "data-dojo-type": "dijit.form.SimpleTextarea",
                "data-dojo-id": "visit_past_history",
                "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-_:0-9#]+','invalidMessage' : 'Invalid Character'"
             }  
}

VISIT_IMAGING_FORM_CONSTANTS = {

          'modality':{
                  'max_length': '100',
                  "data-dojo-type": "dijit.form.Select",
                  "data-dojo-id": "visit_imaging_imaging",
                  "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'finding':{
                  'max_length': '1000',
                  "data-dojo-type": "dijit.form.SimpleTextarea",
                  "data-dojo-id": "visit_imaging_finding",
                  "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          }

}

VISIT_INVESTIGATION_FORM_CONSTANTS = {

          'investigation':{
                        'max_length': '100',
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-id": "visit_investigation_investigation",
                        "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'value':{
                  'max_length': '100',
                  "data-dojo-type": "dijit.form.ValidationTextBox",
                  "data-dojo-id": "visit_investigation_value",
                  "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          }

}


VISIT_ROS_FORM_CONSTANTS = {

          'const_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'eye_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'ent_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'cvs_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'resp_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'gi_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'gu_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'ms_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'integ_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'neuro_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'psych_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'endocr_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'immuno_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          },

          'hemat_symp':{              
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
          }
}

VISIT_FOLLOW_UP_FORM_CONSTANTS = {
 
          'visit_date':{
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.DateTextBox",
                        "data-dojo-props": r"'required' :true"
          },

          'op_surgeon':{
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' : true"
          },

          'consult_nature':{
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' :true"
           },

           'status':{
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' :true"
            },

           "subjective":{
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
            },

           "objective":{
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
            },        

           "assessment":{
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
            },

           "plan":{
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
            }

}

VISIT_SOAP_FORM_CONSTANTS = {

             "subjective":{
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
            },

           "objective":{
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
            },        

           "assessment":{
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
            },

           "plan":{
                        'max_length': '500',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
            }
}