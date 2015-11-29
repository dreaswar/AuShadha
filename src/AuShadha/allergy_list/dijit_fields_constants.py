
ALLERGY_FORM_CONSTANTS = {
    'allergic_to': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' :true ,'regExp':'[\\w]+','invalidMessage':'Invalid Character' "
    },
    'reaction_observed': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' : true "
    }
}
