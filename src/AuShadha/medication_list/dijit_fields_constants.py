MEDICATION_LIST_FORM_CONSTANTS = {
            'medication':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' :'true' ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
            },
            'strength':{
                        'max_length': 3,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
            },
            'dosage':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
            },
            'prescription_date':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.DateTextBox",
                        "data-dojo-props": r"'required' : 'true'"
            },
            'prescribed_by':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
            },
            'currently_active':{
                        'max_length': 2,
                        "data-dojo-type": "dijit.form.CheckBox",
                        "data-dojo-props": r""
            } 
}
