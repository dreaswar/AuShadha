var GRID_STRUCTURES= {
  PATIENT_GRID  : [
                  {name       : "ID", 
                  field      : "id", 
                  width      : "50px",
                  hidden     : true,
                  cellStyles : "text-align:center;"
                  },
                  {name       : "Edit", 
                  field      : "edit", 
                  width      : "50px",
                  hidden     : true,
                  cellStyles : "text-align:center;"
                  },
                  {name       : "Del", 
                  field      : "del", 
                  width      : "50px",
                  hidden     : true,
                  cellStyles : "text-align:center;"
                  },
                  {name       : "Visit", 
                  field      : "visitadd", 
                  width      : "50px",
                  hidden     : true,
                  cellStyles : "text-align:center;"
                  },
                  {name       : "Adm", 
                    field      : "admissionadd", 
                    width      : "50px",
                    hidden     : true,
                    cellStyles : "text-align:center;"
                  },

                  {name       : "Patient ID", 
                    field      : "patient_hospital_id", 
                    width      : "100px",
                    cellStyles : "text-align:center;"
                  },
                  { name      : "First Name", 
                    field     : "first_name", 
                    width      : "100px",
                    cellStyles : "text-align:center;"
                  },
                  { name      : "Middle Name", 
                    field     : "middle_name", 
                    width      : "100px",
                    cellStyles : "text-align:center;"
                  },
                  { name       : "Last Name" ,
                    field      : "last_name" , 
                    width      : "100px",
                    cellStyles : "text-align:center;",
                    formatter  : function(last_name){ 
                                  return '<em>'+ last_name +'</em>';
                               }
                  },
                  { name        : "Full Name", 
                    field       : "full_name", 
                    width       : "100px",
                    hidden      : true,
                    cellStyles  : "text-align:center;"
                  },
                  {name       : "Age"   ,
                    field      : "age"   ,
                    width      : "100px",
                    cellStyles : "text-align:center;"
                  },
                  {name      : "Sex" , 
                    field     : "sex" ,
                    width      : "100px",
                    formatter : function(sex){
                              if(sex == 'Male'){
                               return '<img src="{{STATIC_URL}}images/male.png" '+
                                       'alt="Male" class="small_img">'; 
                              }
                              else if(sex == 'Female'){
                               return '<img '+
                                      'src="{{STATIC_URL}}images/female.png"'+
                                      'title="'+ sex +
                                      '" alt="Male" class="small_img">'; 
                              }
                              else{
                               return "Others"
                              } 
                            },
                    cellStyles: "text-align:center;"
                  },
                  { name      : "URL"   , 
                    field     : "home"  ,
                    width      : "50px",
                    hidden    : true,
                    cellStyles: "text-align:center;",
                  }],

  PATIENT_CONTACT_GRID_STRUCTURE: [
                                {name       : "ID", 
                                 field      : "id", 
                                 width      : "50px",
                                 hidden     : true,
                                 cellStyles : "text-align:center;"
                                },

                                {name       : "PatID", 
                                 field      : "pat_id", 
                                 width      : "50px",
                                 hidden     : true,
                                 cellStyles : "text-align:center;"
                                },

                                {name       : "Edit", 
                                 field      : "edit", 
                                 width      : "50px",
                                 hidden     : true,
                                 cellStyles : "text-align:center;"
                                },

                                {name       : "Del", 
                                 field      : "del", 
                                 width      : "50px",
                                 hidden     : true,
                                 cellStyles : "text-align:center;"
                                },

                                {name       : "Type", 
                                 field      : "address_type", 
                                 width      : "50px",
                                 cellStyles : "text-align:center;"
                                },

                                {name       : "Address", 
                                 field      : "address", 
                                 width      : "250px",
                                 cellStyles : "text-align:center;"
                                },

                                {name       : "City", 
                                 field      : "city", 
                                 width      : "150px",
                                 cellStyles : "text-align:center;"
                                },

                                {name       : "State", 
                                 field      : "state", 
                                 width      : "50px",
                                 cellStyles : "text-align:center;"
                                },

                                {name       : "Country", 
                                 field      : "country", 
                                 width      : "100px",
                                 cellStyles : "text-align:center;"
                                },

                                {name       : "Pincode", 
                                 field      : "pincode", 
                                 width      : "100px",
                                 cellStyles : "text-align:center;"
                                }],

  PATIENT_PHONE_GRID_STRUCTURE: [
                                 {name       : "ID", 
                                   field      : "id", 
                                   width      : "50px",
                                   hidden     : true,
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "Edit", 
                                   field      : "edit", 
                                   width      : "50px",
                                   hidden     : true,
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "Del", 
                                   field      : "del", 
                                   width      : "50px",
                                   hidden     : true,
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "Type", 
                                   field      : "phone_type", 
                                   width      : "50px",
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "ISD", 
                                   field      : "ISD_Code", 
                                   width      : "250px",
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "STD", 
                                   field      : "STD_Code", 
                                   width      : "150px",
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "Phone", 
                                   field      : "phone", 
                                   width      : "50px",
                                   cellStyles : "text-align:center;"
                                  }],

  PATIENT_GUARDIAN_GRID_STRUCTURE: [
                                    {name       : "ID", 
                                      field      : "id", 
                                      width      : "50px",
                                      hidden     : true,
                                      cellStyles : "text-align:center;"
                                    },

                                    {name       : "Edit", 
                                      field      : "edit", 
                                      width      : "50px",
                                      hidden     : true,
                                      cellStyles : "text-align:center;"
                                    },

                                    {name       : "Del", 
                                      field      : "del", 
                                      width      : "50px",
                                      hidden     : true,
                                      cellStyles : "text-align:center;"
                                    },

                                    {name       : "Name", 
                                      field      : "guardian_name", 
                                      width      : "50px",
                                      cellStyles : "text-align:center;"
                                    },

                                    {name       : "Relation", 
                                      field      : "relation_to_guardian", 
                                      width      : "250px",
                                      cellStyles : "text-align:center;"
                                    },

                                    {name       : "Phone", 
                                      field      : "guardian_phone", 
                                      width      : "150px",
                                      cellStyles : "text-align:center;"
                                    }],

  PATIENT_DEMOGRAPHICS_GRID_STRUCTURE: [
                                    {name       : "ID", 
                                      field      : "id", 
                                      width      : "50px",
                                      hidden     : true,
                                      cellStyles : "text-align:center;"
                                    },

                                    {name       : "Edit", 
                                      field      : "edit", 
                                      width      : "50px",
                                      hidden     : true,
                                      cellStyles : "text-align:center;"
                                    },

                                    {name       : "Del", 
                                      field      : "del", 
                                      width      : "50px",
                                      hidden     : true,
                                      cellStyles : "text-align:center;"
                                    },

                                    {name       : "Socioeconomics", 
                                      field      : "socioeconomics", 
                                      width      : "50px",
                                      cellStyles : "text-align:center;"
                                    },

                                    {name       : "Education", 
                                      field      : "education", 
                                      width      : "250px",
                                      cellStyles : "text-align:center;"
                                    },

                                    {name       : "Date of Birth", 
                                      field      : "date_of_birth", 
                                      width      : "150px",
                                      cellStyles : "text-align:center;"
                                    }],

  PATIENT_ALLERGY_GRID_STRUCTURE: "",

  PATIENT_IMMUNIZATION_GRID_STRUCTURE: "",

  PATIENT_PATIENT_MEDIA_GRID_STRUCTURE: "",

  PATIENT_ADMISSION_GRID_SRUCTURE: [
                                  {name       : "ID", 
                                    field      : "id", 
                                    width      : "50px",
                                    hidden     : true,
                                    cellStyles : "text-align:center;"
                                  },

                                  {name       : "Home", 
                                    field      : "home", 
                                    width      : "50px",
                                    hidden     : true,
                                    cellStyles : "text-align:center;"
                                  },

                                  {name       : "Edit", 
                                    field      : "edit", 
                                    width      : "50px",
                                    hidden     : true,
                                    cellStyles : "text-align:center;"
                                  },

                                  {name       : "Del", 
                                    field      : "del", 
                                    width      : "50px",
                                    hidden     : true,
                                    cellStyles : "text-align:center;"
                                  },

                                  {name       : "DOA", 
                                    field      : "date_of_admission", 
                                    width      : "50px",
                                    cellStyles : "text-align:center;"
                                  },

                                  {name       : "TOA", 
                                    field      : "time_of_admission", 
                                    width      : "50px",
                                    cellStyles : "text-align:center;"
                                  },

                                  {name       : "Surgeon", 
                                    field      : "admitting_surgeon", 
                                    width      : "250px",
                                    cellStyles : "text-align:center;"
                                  },

                                  {name       : "Status", 
                                    field      : "admission_closed", 
                                    width      : "150px",
                                    cellStyles : "text-align:center;",
                                    formatter : function(admission_closed){
                                                      if(admission_closed == true){
                                                          return '<img src="{{STATIC_URL}}images/flag_green.png" '+
                                                          'alt="Discharged" class="small_img">'; 
                                                      }
                                                      else if(admission_closed == false){
                                                          return '<img '+
                                                          'src="{{STATIC_URL}}images/flag_green.png"'+
                                                          'alt="Active" class="small_img">'; 
                                                      }
                                                      else{
                                                          return "Others"
                                                      }
                                                } 
                                  },

                                  {name       : "Room", 
                                  field      : "room_or_ward", 
                                  width      : "50px",
                                  cellStyles : "text-align:center;"
                                  },

                                  {name       : "Hospital", 
                                  field      : "hospital", 
                                  width      : "100px",
                                  cellStyles : "text-align:center;"
                                  }],

  PATIENT_VISIT_GRID_STRUCTURE: [
                                  {name       : "ID", 
                                   field      : "id", 
                                   width      : "50px",
                                   hidden     : true,
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "Edit", 
                                   field      : "edit", 
                                   width      : "50px",
                                   hidden     : true,
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "Del", 
                                   field      : "del", 
                                   width      : "50px",
                                   hidden     : true,
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "DOV", 
                                   field      : "visit_date", 
                                   width      : "50px",
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "Surgeon", 
                                   field      : "op_surgeon", 
                                   width      : "250px",
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "Nature", 
                                   field      : "consult_nature", 
                                   width      : "150px",
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "Status", 
                                   field      : "is_active", 
                                   width      : "50px",
                                   cellStyles : "text-align:center;"
                                  },

                                  {name       : "Remarks", 
                                   field      : "remarks", 
                                   width      : "100px",
                                   cellStyles : "text-align:center;"
                                  }],
};

