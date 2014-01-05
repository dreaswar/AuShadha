VISIT_ASSESSMENT_AND_PLAN_FORM_CONSTANTS = {

           "case_summary":{
                        'max_length': '1000',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'",
                        "class" : r"case_summary_textarea"
            },

           "possible_diagnosis":{
                        'max_length': '1000',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'",
                        "class" : r"possible_diagnosis_textarea"
            },

           "plan":{
                        'max_length': '1000',
                        "data-dojo-type": "dijit.form.Textarea",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'",
                        "class" : r"plan_textarea"
            }

}