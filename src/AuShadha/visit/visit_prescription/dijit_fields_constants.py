VISIT_PRESCRIPTION_FORM_CONSTANTS = {
              'medicament':{
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.TextBox",
                        "data-dojo-props": r"'required' :true ,'regExp':'[a-zA-Z\'-. ]+','invalidMessage':'Invalid Character' "
              },
              'middle_name':{
                        'max_length': 100,
                        "data-dojo-type": "dijit.form.TextBox",
                        "data-dojo-props": r"'required' : false ,'regExp':'[a-zA-Z\'-. ]+','invalidMessage' : 'Invalid Character'"
              },
              'allow_substitution':{
                        'max_length': 20,
                        "data-dojo-type": "dijit.form.CheckBox",
                        "data-dojo-props": r"'required' : false "
              },
              'print_prescription':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.CheckBox",
                        "data-dojo-props": r"'required' : true"
              },
              'dispensing_form':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' : true "
              },
              'route':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' : true"
              },

              'start': {
                        'max_length': 0,
                        'data-dojo-type': "dijit.form.DateTimeBox",
                        'data-dojo-props': r" 'required': true "
                       },
 
              'end': {
                        'max_length': 0,
                        'data-dojo-type': "dijit.form.DateTimeBox",
                        'data-dojo-props': r" 'required': true "
                       },

              'treatment_duration': {
                        'max_length': 30,
                        'data-dojo-type': "dijit.form.ValidationTextBox",
                        'data-dojo-props': r"'required': true"},
              
              'dose': {
                        'max_length': 30,
                        'data-dojo-type': "dijit.form.ValidationTextBox",
                        'data-dojo-props': r"'required': true" },

              'dose_unit': {
                       'max_length': 30,
                       'data-dojo-type': "dijit.form.ValidationTextBox",
                       'data-dojo-props': r"'required': true" },

              'units': {
                       'max_length': 20,
                       'data-dojo-type': "dijit.form.NumberSpinner",
                       'data-dojo-props': r"'required': true"},

              'frequency': {
                       'max_length': 250,
                       'data-dojo-type': "dijit.form.TextBox",
                       'data-dojo-props': r"'required': true" },

              'admin_hours': {
                       'max_length': 250,
                       'data-dojo-type': "dijit.form.TextBox",
                       'data-dojo-props': r"'required': true" },

              'review': {
                       'max_length': 20,
                       'data-dojo-type': "dijit.form.DateTimeBox",
                       'data-dojo-props': r"'required': true" },
        
              'refills': {
                       'max_length': 20,
                       'data-dojo-type': "dijit.form.NumberSpinner",
                       'data-dojo-props': r"'required': true" },

              'comment': {
                       'max_length': 300,
                       'data-dojo-type': "dijit.form.TextBox",
                       'data-dojo-props': r"'required': true" }

}              


