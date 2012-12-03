require([
    "dojo/ready",
    "dojo/_base/window",
    "dojo/store/Memory",
    "dijit/tree/ObjectStoreModel",
    "dijit/Tree","dojo/dom"
], function(ready, win, Memory, ObjectStoreModel, Tree,dom){
    // Create store, adding the getChildren() method required by ObjectStoreModel
    var patientTreeStore = new Memory({
        data: [
            { id: 'patient',
              name:'Patient',
              type:'trunk'
            },

              { id: 'contact',
                name:'Contact',
                type:'main_branch',
                parent: 'patient'
              },
                  { id: 'address',
                    name:'Address',
                    type:'second_branch',
                    parent: 'contact'
                  },
                  { id: 'phone',
                    name:'Phone',
                    type:'second_branch',
                    parent: 'contact'
                  },

              { id: 'history',
                name:'History',
                type:'main_branch',
                parent: 'patient'
              },
                  { id: 'demographics',
                    name:'Demographics',
                    type:'second_branch',
                    parent: 'history'
                  },
                  { id: 'social',
                    name:'Social',
                    type:'second_branch',
                    parent: 'history'
                  },
                  { id: 'family',
                    name:'Family',
                    type:'second_branch',
                    parent: 'history'
                  },
                  { id: 'medical_and_surgical_history',
                    name:'Medical & Surgical ',
                    type:'second_branch',
                    parent: 'history'
                  },
                      { id: 'medical_history',
                        name:'Medical History',
                        type:'third_branch',
                        parent: 'medical_and_surgical_history'
                      },
                      { id: 'surgical_history',
                        name:'Surgical History',
                        type:'third_branch',
                        parent: 'medical_and_surgical_history'
                      },

              { id: 'preventive_health',
                name:'Preventive Health',
                type:'main_branch',
                parent: 'patient'
              },
                  { id: 'neonatal_and_paediatric_preventives',
                    name:'Neonatal & Paediatric',
                    type:'second_branch',
                    parent: 'preventive_health'
                  },
                  { id: 'immunisation',
                    name:'Immunisation',
                    type:'second_branch',
                    parent: 'preventive_health'
                  },
                  { id: 'obstetric_preventives',
                    name:'Obstetrics',
                    type:'second_branch',
                    parent: 'preventive_health'
                  },
                  { id: 'gynaecology_preventives',
                    name:'Gynaecology',
                    type:'second_branch',
                    parent: 'preventive_health'
                  },
                  { id: 'medical_and_surgical_preventives',
                    name:'Medical & Surgical',
                    type:'second_branch',
                    parent: 'preventive_health'
                  },

              { id: 'medication_and_allergies',
                name:'Medications & Allergies',
                type:'main_branch',
                parent: 'patient'
              },

                  { id: 'medication_list',
                    name:'Medication List',
                    type:'second_branch',
                    parent: 'medication_and_allergies'
                  },
                  { id: 'allergy_list',
                    name:'Allergy List',
                    type:'second_branch',
                    parent: 'medication_and_allergies'
                  },

              { id: 'admissions_and_visits',
                name:'Admissions & Visits',
                type:'main_branch',
                parent: 'patient'
              },

                  { id: 'patient_admissions',
                    name:'Admissions',
                    type:'second_branch',
                    parent: 'admissions_and_visits'
                  },
                  { id: 'patient_visits',
                    name:'Visits',
                    type:'second_branch',
                    parent: 'admissions_and_visits'
                  },

              { id: 'patient_media',
                name:'Media',
                type:'main_branch',
                parent: 'patient'
              },

                  { id: 'patient_documents',
                    name:'Documents',
                    type:'second_branch',
                    parent: 'patient_media'
                  },
                  { id: 'patient_images',
                    name:'Images',
                    type:'second_branch',
                    parent: 'patient_media'
                  },
                  { id: 'patient_videos',
                    name:'Videos',
                    type:'second_branch',
                    parent: 'patient_media'
                  }
        ],
        getChildren: function(object){
            return this.query({parent: object.id});
        }
    });

    // Create the model
    var patientTreeModel = new ObjectStoreModel({
        store: patientTreeStore,
        query: {id: 'patient'}
    });

    // Create the Tree.
    ready(function(){
        var patientTree = new Tree({
            model: patientTreeModel
        });
        //patientTree.placeAt(win.body());
        patientTree.placeAt('patientTreeContainer')
        patientTree.startup();
    });
});
