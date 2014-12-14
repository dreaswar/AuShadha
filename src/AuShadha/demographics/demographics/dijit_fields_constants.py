
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