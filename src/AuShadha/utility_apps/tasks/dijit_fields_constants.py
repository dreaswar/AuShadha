#DEFINE ALL THE FORMS HERE AS JSON
#DEFINITIONS ARE LOADED AS DIJIT WIDGETS
#VARIABLES LISTED HERE AS DICTIONARY NEEDS TO BE IMPORTED BACK INTO MODELS.PY WHEN FORMS ARE DEFINED

TASK_DETAIL_FORM_CONSTANTS = {
              'name':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.ValidationTextBox",
                        "data-dojo-props": r"'required' :true ,'regExp':'[a-zA-Z\'-. ]+','invalidMessage':'Invalid Character' "
              },
              'description':{
                        'max_length': 1000,
                        "data-dojo-type": "dijit.form.TextBox",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z\'-. ]+','invalidMessage' : 'Invalid Character'"
              },
              'deadline':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.DateBox",
                        "data-dojo-props": r"'required' : true ,'regExp':'[a-zA-Z\'-. ]+','invalidMessage' : 'Invalid Character'"
              },
              'priority':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' : true ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
              },
              'status':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' : true ,'regExp':'\\d{1,3}','invalidMessage' : 'Invalid Charected chosen!'"
              },
              'assigned_to':{
                        'max_length': 30,
                        "data-dojo-type": "dijit.form.Select",
                        "data-dojo-props": r"'required' : true ,'regExp':'[\\w]+','invalidMessage' : ''"
              }
}
