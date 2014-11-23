GUARDIAN_FORM_CONSTANTS = {

    'guardian_name':{'max_length': 30,
                    "data-dojo-type": "dijit.form.ValidationTextBox",
                    "data-dojo-props": r"'required' :'true' ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
                    },

    'relation_to_guardian':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
                        },

    'guardian_phone':{
                      'max_length': 30,
                      "data-dojo-type": "dijit.form.ValidationTextBox",
                      "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
                      }

}