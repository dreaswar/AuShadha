VISIT_PRESCRIPTION_FORM_CONSTANTS = {

    'medicament': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' :true ,'regExp':'[a-zA-Z\'-. ]+','invalidMessage':'Invalid Character' "
    },

    'indication': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' : false ,'regExp':'[a-zA-Z\'-. ]+','invalidMessage' : 'Invalid Character'"
    },

    'allow_substitution': {
        'max_length': 20,
        "data-dojo-type": "dijit.form.CheckBox",
        "data-dojo-props": r"'required' : false "
    },

    'print_prescription': {
        'max_length': 30,
        "data-dojo-type": "dijit.form.CheckBox",
        "data-dojo-props": r"'required' : false"
    },

    'dispensing_form': {
        'max_length': 30,
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' : true "
    },

    'route': {
        'max_length': 30,
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' : true"
    },

    'start_date': {
        'max_length': 0,
        'data-dojo-type': "dijit.form.DateTextBox",
        'data-dojo-props': r" 'required': false "
    },

    'end_date': {
        'max_length': 0,
        'data-dojo-type': "dijit.form.DateTextBox",
        'data-dojo-props': r" 'required': false "
    },

    'treatment_duration': {
        'max_length': 30,
        'data-dojo-type': "dijit.form.ValidationTextBox",
        'data-dojo-props': r"'required': true"
    },

    'dose': {
        'max_length': 30,
        'data-dojo-type': "dijit.form.ValidationTextBox",
        'data-dojo-props': r"'required': true"
    },

    'dose_unit': {
        'max_length': 30,
        'data-dojo-type': "dijit.form.Select",
        'data-dojo-props': r"'required': true"
    },

    'units': {
        'max_length': 20,
        'data-dojo-type': "dijit.form.NumberSpinner",
        "data-dojo-props": r"'required' : false, placeHolder:'max of 200',smallDelta:'1', constraints:{min:0,max:200,places:0}"
    },

    'frequency': {
        'max_length': 250,
        'data-dojo-type': "dijit.form.Select",
        'data-dojo-props': r"'required': true"
    },

    'admin_hours': {
        'max_length': 250,
        'data-dojo-type': "dijit.form.Textarea",
        'data-dojo-props': r"'required': false"
    },

    'review': {
        'max_length': 20,
        'data-dojo-type': "dijit.form.DateTextBox",
        'data-dojo-props': r"'required': false"
    },

    'refills': {
        'max_length': 20,
        'data-dojo-type': "dijit.form.NumberSpinner",
        "data-dojo-props": r"'required' : false, placeHolder :'max of 5', smallDelta:'1', constraints: {min:0,max:5,places:0}"
    },

    'comment': {
        'max_length': 300,
        'data-dojo-type': "dijit.form.Textarea",
        'data-dojo-props': r"'required': false"
    }

}
