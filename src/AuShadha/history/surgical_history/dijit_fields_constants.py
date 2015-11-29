SURGICAL_HISTORY_FORM_CONSTANTS = {
    'base_condition': {
        'max_length': 500,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' :false"
    },
    'description': {
        'max_length': 1000,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' :true"
    },
    'classification': {
        'max_length': 200,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' :false,placeHolder:'Any other Classification..'"
    },
    'date_of_surgery': {
        "data-dojo-type": "dijit.form.DateTextBox",
        "data-dojo-props": r"'required' : false"
    },
    'icd_10': {
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' :false"
    },
    'icd_10_pcs': {
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' : false"
    },
    'healed': {
        "data-dojo-type": "dijit.form.CheckBox",
        "data-dojo-props": r"'required' :false"
    },

    'remarks': {
        'max_length': 1000,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' : false"
    }
}
