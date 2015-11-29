SOCIAL_HISTORY_FORM_CONSTANTS = {
    'marital_status': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Select",
                          "data-dojo-props": r"'required' :true"
    },
    'marital_status_notes': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.ValidationTextBox",
                          "data-dojo-props": r"'required' :false ,placeHolder:'Any Other Notes...'"
    },
    'occupation': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Select",
                          "data-dojo-props": r"'required' : true"
    },
    'occupation_notes': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.ValidationTextBox",
                          "data-dojo-props": r"'required' :false,placeHolder:'Others '"
    },
    'exercise': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Select",
                          "data-dojo-props": r"'required' : true"
    },
    'exercise_notes': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.ValidationTextBox",
                          "data-dojo-props": r"'required' :false,placeHolder:'Other Notes...'"
    },
    'diet': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' : true"
    },
    'diet_notes': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.ValidationTextBox",
                          "data-dojo-props": r"'required' :false,placeHolder:'Specify'"
    },
    'home_occupants': {
        'max_length': 150,
        "data-dojo-type": "dijit.form.MultiSelect",
                          "data-dojo-props": r"'required' : true"
    },
    'home_occupants_notes': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.ValidationTextBox",
                          "data-dojo-props": r"'required' :false,placeHolder:'Other details ?'"
    },
    'pets': {
        'max_length': 150,
        "data-dojo-type": "dijit.form.MultiSelect",
        "data-dojo-props": r"'required' : true"
    },
    'pets_notes': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' :false,placeHolder:'Notes'"
    },
    'alcohol': {
        'max_length': 150,
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' : true"
    },
    'alcohol_no': {
        'max_length': "",
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' :false"
    },
    'alcohol_notes': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' :false,placeHolder:'Any Other Notes...'"
    },
    'tobacco': {
        'max_length': 150,
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' : true"
    },
    'tobacco_no': {
        'max_length': "",
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' :false"
    },
    'tobacco_notes': {
        'max_length': 200,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' :false,placeHolder:'Any Other Notes...'"
    },
    'drug_abuse': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' : true"
    },
    'drug_abuse_notes': {
        'max_length': 150,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' : false,placeHolder:'Details..'"
    },
    'sexual_preference': {
        'max_length': 100,
        "data-dojo-type": "dijit.form.Select",
        "data-dojo-props": r"'required' : true"
    },
    'sexual_preference_notes': {
        'max_length': 250,
        "data-dojo-type": "dijit.form.ValidationTextBox",
        "data-dojo-props": r"'required' : false,placeHolder:'Other details'"
    },
    'current_events': {
        'max_length': 250,
        "data-dojo-type": "dijit.form.Textarea",
        "data-dojo-props": r"'required' : false,placeHolder:'Notes about specific events in family that has bearing on treatment'"
    }
}
