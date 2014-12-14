VISIT_DETAIL_FORM_CONSTANTS = {
  'visit_date':{
                'max_length': 100,
                "data-dojo-type": "dijit.form.DateTextBox",
                "data-dojo-props": r"'required' :true"
  },
#  'op_surgeon':{
#                'max_length': 100,
#                "data-dojo-type": "dijit.form.Select",
#                "data-dojo-props": r"'required' : true"
#  },
  'referring_doctor':{
                'max_length': 100,
                "data-dojo-type": "dijit.form.ValidationTextBox",
                "data-dojo-props": r"'required' :false"
  },
  'consult_nature':{
                'max_length': 100,
                "data-dojo-type": "dijit.form.Select",
                "data-dojo-props": r"'required' :true"
  },
  'booking_category':{
                'max_length': 100,
                "data-dojo-type": "dijit.form.Select",
                "data-dojo-props": r"'required' :true"
  },
  'consult_reason':{
                'max_length': 100,
                "data-dojo-type": "dijit.form.Select",
                "data-dojo-props": r"'required' :true"
  },
  'status':{
              'max_length': 100,
              "data-dojo-type": "dijit.form.Select",
              "data-dojo-props": r"'required' :true"
  },
  'remarks':{
              'max_length': 150,
              "data-dojo-type": "dijit.form.Textarea",
              "data-dojo-props": r"'required' :false"
  }
}
