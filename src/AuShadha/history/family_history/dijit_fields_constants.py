FAMILY_HISTORY_FORM_CONSTANTS = {
    'family_member': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' :true ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
    },
    'disease': {
        'max_length': 150,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' : false ,'regExp':'[\\w]+','invalidMessage' : 'Invalid Character'"
    },
    'age_at_onset': {
        'max_length': 30,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' : false ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
    },
    'deceased': {
        'max_length': 2,
        "data-dojo-type": "dijit.form.CheckBox",
        "data-dojo-props": r""
    },
    'age': {
        'max_length': 30,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' : false ,'regExp':'[\\d]+','invalidMessage' : 'Invalid Character'"
    }
}
