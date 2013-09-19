
GUARDIAN_FORM_CONSTANTS = {

                        'guardian_name':{'max_length': 30,
                                        "data-dojo-type": "dijit.form.ValidationTextBox",
                                        "data-dojo-props": r"'required' :'true' ,\
                                                             'regExp':'[\\w]+',\
                                                             'invalidMessage':'Invalid Character' "
                                        },

                        'relation_to_guardian':{
                                            'max_length': 30,
                                            "data-dojo-type": "dijit.form.Select",
                                            "data-dojo-props": r"'required' : 'true' ,\
                                                                 'regExp':'[\\w]+',\
                                                                 'invalidMessage' : 'Invalid Character'"
                                            },

                        'guardian_phone':{
                                          'max_length': 30,
                                          "data-dojo-type": "dijit.form.ValidationTextBox",
                                          "data-dojo-props": r"'required' : 'true' ,\
                                                               'regExp':'[\\w]+',\
                                                               'invalidMessage' : 'Invalid Character'"
                                          }

}

CONTACT_FORM_CONSTANTS = {

                        'address_type':{'max_length': 30,
                                        "data-dojo-type": "dijit.form.Select",
                                        "data-dojo-props": r"'required' :'true' ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
                                      },

                        'address':{'max_length': 100,
                                    "data-dojo-type": "dijit.form.Textarea",
                                    "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z0-9-:;/\#_]','invalidMessage' : 'Invalid Character'"
                                    },

                        'city':{'max_length': 30,
                              "data-dojo-type": "dijit.form.ValidationTextBox",
                              "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z -]+','invalidMessage' : 'Invalid Character'"
                              },

                        'state':{'max_length': 30,
                                "data-dojo-type": "dijit.form.ValidationTextBox",
                                "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z -]+','invalidMessage' : 'Invalid Character'"
                            },

                        'pincode':{'max_length': 7,
                                  "data-dojo-type": "dijit.form.ValidationTextBox",
                                  "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
                            },

                        'country':{
                            'max_length': 30,
                            "data-dojo-type": "dijit.form.ValidationTextBox",
                            "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : ''"
                            }
}

PHONE_FORM_CONSTANTS = {
                      'ISD_Code':{
                                  'max_length': 5,
                                  "data-dojo-type": "dijit.form.ValidationTextBox",
                                  "data-dojo-props": r"'required' :'true' ,'regExp':'[\\d]+','invalidMessage':'Invalid Character' "
                      },

                      'STD_Code':{
                                'max_length': 6,
                                "data-dojo-type": "dijit.form.ValidationTextBox",
                                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
                      },

                      'phone':{
                                'max_length': 15,
                                "data-dojo-type": "dijit.form.ValidationTextBox",
                                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
                      },

                      'phone_type':{
                                'max_length': 30,
                                "data-dojo-type": "dijit.form.Select",
                                "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
                      }
}

DEMOGRAPHICS_FORM_CONSTANTS = {
  
                      'date_of_birth':{
                                      'max_length': 30,
                                      "data-dojo-type": "dijit.form.DateTextBox",
                                      "data-dojo-props": r"'required' :true ,'regExp':'','invalidMessage':'Invalid Character' "
                      },

                      'socioeconomics':{
                                      'max_length': 30,
                                      "data-dojo-type": "dijit.form.Select",
                                      "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
                      },
                      
                      'education':{
                                    'max_length': 30,
                                    "data-dojo-type": "dijit.form.Select",
                                    "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
                      },
                      
                      'housing_conditions':{
                                            'max_length': 100,
                                            "data-dojo-type": "dijit.form.Textarea",
                                            "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
                      },
                      
                      'religion':{
                                    'max_length': 30,
                                    "data-dojo-type": "dijit.form.ValidationTextBox",
                                    "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : ''"
                      },
                      
                      'religion_notes':{
                                        'max_length': 100,
                                        "data-dojo-type": "dijit.form.ValidationTextBox",
                                        "data-dojo-props": r"'required' :false,placeHolder:'Any Other Notes...'"
                      },
                      
                      "race":{
                              "max_length": 30,
                              "data-dojo-type": "dijit.form.ValidationTextBox",
                              "data-dojo-props": r"'required':true, 'regExp': '', 'invalidMessage': 'Please select a value' "
                      },
                      
                      "languages_known":{
                                        "max_length": 100,
                                        "data-dojo-type": "dijit.form.Textarea",
                                        "data-dojo-props": r"'required':true, 'regExp': '', 'invalidMessage': 'Please select a value' "
                      }
}

EMAIL_AND_FAX_FORM_CONSTANTS = {
  
}