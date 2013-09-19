
MEDICAL_HISTORY_FORM_CONSTANTS ={
  
  'disease':{
            'max_length': 100,
            "data-dojo-type": "dijit.form.ValidationTextBox",
            "data-dojo-props": r"'required' :true"
  },
  'icd_10':{
                "max_length":150,
                "data-dojo-type": "dijit.form.ValidationTextBox",
                "data-dojo-props": r"'required' :false"
  },
  'status':{
              "max_length" : 500,
              "data-dojo-type": "dijit.form.Textarea",
              "data-dojo-props": r"'required' : false"
  },
  'infectious_disease':{
              "data-dojo-type": "dijit.form.CheckBox",
              "data-dojo-props": r"'required' :false"
  },
  'active':{
            "data-dojo-type": "dijit.form.CheckBox",
            "data-dojo-props": r"'required' : false"
  },
  'severity':{
            'max_length': 100,
            "data-dojo-type": "dijit.form.ValidationTextBox",
            "data-dojo-props": r"'required' :false,placeHolder:'Severity of disease'"
  },
  'allergic_disease':{
            "data-dojo-type": "dijit.form.CheckBox",
            "data-dojo-props": r"'required' : false"
  },
  'pregnancy_warning':{
            "data-dojo-type": "dijit.form.CheckBox",
            "data-dojo-props": r"'required' :false"
  },
  'date_of_diagnosis':{
              "data-dojo-type": "dijit.form.DateTextBox",
              "data-dojo-props": r"'required' : false"
  },
  'healed':{
            "data-dojo-type": "dijit.form.CheckBox",
            "data-dojo-props": r"'required' :false"
  },
  'remarks':{
            'max_length': 1000,
            "data-dojo-type": "dijit.form.Textarea",
            "data-dojo-props": r"'required' : false"
  }
}