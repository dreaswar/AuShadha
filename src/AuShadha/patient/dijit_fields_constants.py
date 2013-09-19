PATIENT_DETAIL_FORM_CONSTANTS = {
              'first_name':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' :'true' ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
              },
              'middle_name':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
              },
              'last_name':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
              },
              'patient_hospital_id':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : 'true' ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
              },
              'age':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : 'true' ,'regExp':'\\d{1,3}','invalidMessage' : 'Invalid Character. Only Numbers are allowed'"
              },
              'sex':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' : 'true' ,'regExp':'','invalidMessage' : ''"
              }
              #,
              #"parent_clinic":{
                           #"max_length": 30,
                           #"data-dojo-type": "dijit.form.Select",
                           #"data-dojo-props": r"'required':'true', 'regExp': '', 'invalidMessage': 'Please select a value' "
              #}
}