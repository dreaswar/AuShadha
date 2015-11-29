IMMUNISATION_FORM_CONSTANTS = {'vaccine_detail': {
    'max_length': 30,
    "data-dojo-type": "dijit.form.FilteringSelect",
    "data-dojo-props": r"'required': true"
},
    'route': {
    'max_length': 30,
    "data-dojo-type": "dijit.form.Select",
    "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
},
    'injection_site': {
    'max_length': 30,
    "data-dojo-type": "dijit.form.Select",
    "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
},
    'dose': {
    'max_length': 30,
    "data-dojo-type": "dijit.form.FilteringSelect",
    "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
},
    #'administrator':{
    #'max_length': 30,
    #"data-dojo-type": "dijit.form.Select",
    #"data-dojo-props": r"'required': true"
    #},
    'vaccination_date': {
    'max_length': 30,
    "data-dojo-type": "dijit.form.DateTextBox",
    "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
},
    'next_due': {
    'max_length': 30,
    "data-dojo-type": "dijit.form.DateTextBox",
    "data-dojo-props": r"'required' : true ,'regExp':'','invalidMessage' : 'Invalid Character'"
},
    'adverse_reaction': {
    'max_length': 150,
    "data-dojo-type": "dijit.form.Textarea",
    "data-dojo-props": r"'required' : true ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
}
}
