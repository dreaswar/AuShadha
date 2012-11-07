
function setupContactGrid(url){
  require(["dojox/grid/DataGrid", "dojo/store/JsonRest","dojo/data/ObjectStore"], 
  function(DataGrid, JsonRest, ObjectStore, registry){
    var Cstore   = new JsonRest({target:url});
    console.log(Cstore);
    console.log("Creating the Contact Grid")
    var contactGrid = new DataGrid({
                  store         : dataStore = ObjectStore({
                                             objectStore: Cstore
                                  }),
                  selectionMode : "single",
                  rowSelector   : "20px",
                  structure     : GRID_STRUCTURES.PATIENT_CONTACT_GRID_STRUCTURE,
                  noDataMessage : "<span class='dojoxGridNoData'>No Contact Information in Store..</span>"
                }, 
                "contact_list"
    );

    contactGrid.onRowDblClick = function(e){ 
    //  {% if perms.patient.change_patientcontact or perms.patient.delete_patientcontact %}
                      onPatientSubMenuRowClick(e,
                                               contactGrid, 
                                               "Edit Contact"
                                              );
    //  {%endif%}
                      return false; 
    };
    contactGrid.startup();

    console.log("Finished creating Contact Grid");
  });
}


function setupPhoneGrid(url){
  require(["dojox/grid/DataGrid", "dojo/store/JsonRest","dojo/data/ObjectStore"], 
  function(DataGrid, JsonRest, ObjectStore){
    var store   = new JsonRest({target:url});
    var phoneGrid = new DataGrid({
                    store         : dataStore = ObjectStore({
                                               objectStore: store
                                    }),
                    selectionMode : "single",
                    rowSelector   : "20px",
                    structure     : GRID_STRUCTURES.PATIENT_PHONE_GRID_STRUCTURE,
                  noDataMessage   : "<span class='dojoxGridNoData'>No Phone Numbers in Store..</span>"
              }, 
              "phone_list"
      );

      phoneGrid.onRowDblClick = function(e){ 
      // {% if perms.patient.change_patientphone or perms.patient.delete_patientphone %}
                                onPatientSubMenuRowClick(e,phoneGrid, "Edit Phone");
                                return false; 
      // {% endif %}
      };
    phoneGrid.startup();
})
}

function setupGuardianGrid(url){
  require(["dojox/grid/DataGrid", "dojo/store/JsonRest","dojo/data/ObjectStore"], 
  function(DataGrid, JsonRest, ObjectStore){
    var store   = new JsonRest({target:url});
      var guardianGrid = new DataGrid({
                              store         : dataStore = ObjectStore({
                                                       objectStore: store
                                              }),
                              selectionMode : "single",
                              rowSelector   : "20px",
                              structure     : GRID_STRUCTURES.PATIENT_GUARDIAN_GRID_STRUCTURE,
                              noDataMessage : "<span class='dojoxGridNoData'>No Guardian Information in Store..</span>"
                            }, 
                          "guardian_list"
      );

      guardianGrid.onRowDblClick = function(e){ 
      // {% if perms.patient.change_patientguardian or perms.patient.delete_patientguardian %}
                                      onPatientSubMenuRowClick(e,guardianGrid, "Edit Guardian");
                                      return false; 
      // {% endif %}
      };
    guardianGrid.startup();
})
}


function setupAllergiesGrid(url){
  require(["dojox/grid/DataGrid", "dojo/store/JsonRest","dojo/data/ObjectStore"], 
  function(DataGrid, JsonRest, ObjectStore){
     console.log("Setting up Allergy Grid with URL: " + url)
     var store   = new JsonRest({target:url});
     var allergiesGrid = new DataGrid({
                    store           : dataStore = ObjectStore({
                                               objectStore: store
                                      }),
                    selectionMode   : "single",
                    rowSelector     : "20px",
                    structure       : GRID_STRUCTURES.PATIENT_ALLERGIES_GRID_STRUCTURE,
                    noDataMessage   : "<span class='dojoxGridNoData'>No Allergies in Store..</span>"
              }, 
              "allergy_list"
      );

    console.log(allergiesGrid);

    allergiesGrid.onRowDblClick = function(e){ 
    // {% if perms.patient.change_patientallergies or perms.patient.delete_patientallergies %}
                              onPatientSubMenuRowClick(e,allergiesGrid, "Edit Allergy");
                              return false; 
    // {% endif %}
    };

    allergiesGrid.startup();

  });
}

function setupMedicationListGrid(url){
  require(["dojox/grid/DataGrid", "dojo/store/JsonRest","dojo/data/ObjectStore"], 
  function(DataGrid, JsonRest, ObjectStore){
    var store   = new JsonRest({target:url});
     var medicationListGrid = new DataGrid({
                    store         : dataStore = ObjectStore({
                                               objectStore: store
                                    }),
                    selectionMode : "single",
                    rowSelector   : "20px",
                    structure     : GRID_STRUCTURES.PATIENT_MEDICATION_LIST_GRID_STRUCTURE,
                  noDataMessage   : "<span class='dojoxGridNoData'>No Medications  Recorded..</span>"
              }, 
              "medication_list"
      );

      medicationListGrid.onRowDblClick = function(e){ 
      // {% if perms.patient.change_patientmedicationlist or perms.patient.delete_patientmedicationlist %}
                                onPatientSubMenuRowClick(e,medicationListGrid, "Edit Medication List");
                                return false; 
      // {% endif %}
      };
    medicationListGrid.startup();

})
}

function setupFamilyHistoryGrid(url){
  require(["dojox/grid/DataGrid", "dojo/store/JsonRest","dojo/data/ObjectStore"], 
  function(DataGrid, JsonRest, ObjectStore){
    var store   = new JsonRest({target:url});
     var familyHistoryGrid = new DataGrid({
                    store         : dataStore = ObjectStore({
                                               objectStore: store
                                    }),
                    selectionMode : "single",
                    rowSelector   : "20px",
                    structure     : GRID_STRUCTURES.PATIENT_FAMILY_HISTORY_GRID_STRUCTURE,
                  noDataMessage   : "<span class='dojoxGridNoData'>No Family History Recorded..</span>"
              }, 
              "family_history_list"
      );

      familyHistoryGrid.onRowDblClick = function(e){ 
      // {% if perms.patient.change_patientfamilyhistory or perms.patient.delete_patientfamilyhistory %}
                                onPatientSubMenuRowClick(e,familyHistoryGrid, "Edit Family History");
                                return false; 
      // {% endif %}
      };

    familyHistoryGrid.startup();
})
}

function setupImmunisationGrid(url){
  require(["dojox/grid/DataGrid", "dojo/store/JsonRest","dojo/data/ObjectStore"], 
  function(DataGrid, JsonRest, ObjectStore){
   var store   = new JsonRest({target:url});
   var immunisationGrid = new DataGrid({
                  store         : dataStore = ObjectStore({
                                             objectStore: store
                                  }),
                  selectionMode : "single",
                  rowSelector   : "20px",
                  structure     : GRID_STRUCTURES.PATIENT_IMMUNIZATION_GRID_STRUCTURE,
                noDataMessage   : "<span class='dojoxGridNoData'>No Immunisations Recorded..</span>"
            }, 
            "immunisation_list"
    );

    immunisationGrid.onRowDblClick = function(e){ 
    // {% if perms.patient.change_patientimmunisation or perms.patient.delete_patientimmunisation %}
                              onPatientSubMenuRowClick(e,immunisationGrid, "Edit Immunisation");
                              return false; 
    // {% endif %}
    };
    immunisationGrid.startup();
})
}

function setupAdmissionGrid(url){
  require(["dojox/grid/DataGrid", "dojo/store/JsonRest","dojo/data/ObjectStore"], 
  function(DataGrid, JsonRest, ObjectStore){
    var store   = new JsonRest({target:url});
    var admissionGrid = new DataGrid({
                            store         : dataStore = ObjectStore({
                                                         objectStore: store
                                            }),
                            selectionMode : "single",
                            rowSelector   : "20px",
                            clientSort    : false,
                            headerStyle   : ['text-align:center;'],
                            structure     : GRID_STRUCTURES.PATIENT_ADMISSION_GRID_SRUCTURE,
                            noDataMessage : "<span class='dojoxGridNoData'>No Admission Information in Store..</span>",
                        }, 
                        "admission_list"
      );

      admissionGrid.onRowDblClick = function(e){
       //  {% if perms.admission.change_admissiondetail or perms.admission.delete_admissiondetail %}
                                      onPatientSubMenuRowClick(e,
                                                               admissionGrid, 
                                                               "Edit Admission"
                                                              );
                                      return false; 
      // {% endif %}
      };

      admissionGrid.onRowClick   = function(e){ 
        //  {% if perms.admission %}
                                    var topContentPane = registry.byId('centerTopTabPane');
                                    var newTabPane     = registry.byId("admissionHomeContentPane");
                                    console.log(newTabPane)
                                    var item           = admissionGrid.getItem(e.rowIndex);
                                    var homeUrl        = admissionGrid.store.getValue(item,'home')
                                    console.log(homeUrl)
                                    xhr.get({
                                         url    : homeUrl,
                                         load   : function(content){
                                                    newTabPane.set('content', content)
                                                    topContentPane.selectChild(newTabPane);
                                                  }
                                    });
                                    return false; 
        //  {% endif %}
      };
    admissionGrid.startup();
})
}

//{% comment %}
 /*
function setupVisitGrid(url){
  require(["dojox/grid/DataGrid", "dojo/store/JsonRest","dojo/data/ObjectStore"], 
  function(DataGrid, JsonRest, ObjectStore){
    var store   = new JsonRest({target:url});
    var visitGrid = new DataGrid({
                              store         : dataStore = ObjectStore({objectStore: store
                                              }),
                              selectionMode : "single",
                              rowSelector   : "20px",
                              structure     : GRID_STRUCTURES.PATIENT_VISIT_GRID_STRUCTURE,
                              noDataMessage : "<span class='dojoxGridNoData'>No Visit Information in Store..</span>"
                              }, 
                              "visit_list"
    );

    visitGrid.onRowDblClick = function(e){ 
    //{% if perms.visit.change_visitdetail or perms.visit.delete_visitdetail %}
                                   onPatientSubMenuRowClick(e,visitGrid, "Edit Visit");
    //{% endif %}
                                   return false; 
    };
})
}
*/
//{% endcomment %}

 function onPatientSubMenuRowClick(e, gridToUse, titleToUse){ 
      var idx = e.rowIndex,
          item = gridToUse.getItem(idx);
      var contactid = gridToUse.store.getValue(item, "id");
      var edit      = gridToUse.store.getValue(item, "edit");
      var del       = gridToUse.store.getValue(item, "del");
      gridToUse.selection.clear();
      gridToUse.selection.setSelected(item, true);
      xhr.get({
          url  : edit,
          load : function(html, idx){
          var myDialog = dijit.byId("editPatientDialog");
          if(myDialog == undefined || myDialog == null){
            myDialog = new dijit.Dialog({
                              title: titleToUse,
                              content: html,
                              style: "width: 500px; height:500px;"
                             }, "editPatientDialog");
            myDialog.startup();
          }
          else{
            myDialog.set('content', html);
            myDialog.set('title', titleToUse); 
          }
          myDialog.show();
          }
      });
    return false; 
 };

function reInitBottomPanels(){
  console.log("Running function to destroy existing widgets...");
  require(["dijit/registry","dojo/dom","dojo/dom-construct","dojo/dom-style"], 
  function(registry, dom, domConstruct, domStyle){
      var contactTable        = registry.byId("contact_list"),
          phoneTable          = registry.byId("phone_list"),
          guardianTable       = registry.byId("guardian_list"),
//        demographicsTable   = registry.byId("demographics_list"),
//        demographicsForm    = registry.byId("newDemographicsDataAddOrEditForm"),
          allergyTable        = registry.byId("allergy_list"),
          immunizationTable   = registry.byId("immunisation_list"),
          familyHistoryTable  = registry.byId("family_history_list"),
//        socialHistoryTable  = registry.byId("social_history_list"),
          medicationListTable = registry.byId("medication_list"),
          admissionTable      = registry.byId("admission_list"),
          visitTable          = registry.byId("visit_list"),
          patientMediaTable   = registry.byId("patient_media_list");

      if(contactTable){
        contactTable.destroyRecursive();
        console.log("Recreating Contact tab");
        domConstruct.place("<div id='contact_list'></div>",
                           "patientContactTab", 
                           'second'
                           );
        
      }
      if(phoneTable){
        phoneTable.destroyRecursive();
        console.log("Recreating Phone tab");
        domConstruct.place("<div id='phone_list'></div>",
                           "patientContactTab", 
                           'third'
                           );
        
      }
      if(guardianTable){
        guardianTable.destroyRecursive();
        console.log("Recreating Guardian tab");
        domConstruct.place("<div id='guardian_list'></div>",
                           "patientDemographicsTab", 
                           'last'
                           );
        
      }

      if(medicationListTable){
        medicationListTable.destroyRecursive();
        console.log("Recreating Medication List tab");
        domConstruct.place("<div id='medication_list' class='patientContextTabs'></div>",
                           "patientMedicationListAndAllergiesTab", 
                           'second'
                           );
        
      }

      if(allergyTable){
        allergyTable.destroyRecursive();
        console.log("Recreating allergy tab");
        domConstruct.place("<div id='allergy_list' class='patientContextTabs'></div>",
                           "patientMedicationListAndAllergiesTab", 
                           'second'
                           );
        
      }
      if(immunizationTable){
        immunizationTable.destroyRecursive();
        console.log("Recreating immunisation tab");
        domConstruct.place("<div id='immunisation_list' class='patientContextTabs'></div>",
                           "patientImmunisationTab", 
                           'second'
                           );
        
      }

      if(familyHistoryTable){
        familyHistoryTable.destroyRecursive();
        console.log("Recreating Family History tab");
        domConstruct.place("<div id='family_history_list' class='patientContextTabs'></div>",
                           "patientFamilyHistoryTab", 
                           'third'
                           );
        
      }
      if(patientMediaTable){
        patientMediaTable.destroyRecursive();
        console.log("Recreating Patient Media tab");
        domConstruct.place("<div id='patient_media_list' class='patientContextTabs'></div>",
                           "patientMediaTab", 
                           'second'
                           );
        
      }
      if(admissionTable){
        admissionTable.destroyRecursive();
        console.log("Recreating Admission tab");
        domConstruct.place("<div id='admission_list' class='patientContextTabs'></div>",
                           "patientAdmissionAndVisitsTab", 
                           'third'
                           );
        
      }
      if(visitTable){
        visitTable.destroyRecursive();
        console.log("Recreating Visit tab tab");
        domConstruct.place("<div id='visit_list' class='patientContextTabs'></div>",
                           "patientAdmissionAndVisitsTab", 
                           'second'
                           );
      }
   });
}

function cleanUpAdmissionPane(){
  var center_top_pane = dijit.byId('centerTopTabPane');
//      var admission_pane  = dijit.findWidgets("admissionHomeContentPane")
  center_top_pane.selectChild(patientHomeContentPane);
  dojo.forEach(admissionHomeContentPane, function(e){e.destroyRecursive(true)})
  admissionHomeContentPane.domNode.innerHTML = 
      "Please select an admission to display details here."
}

function cleanUpVisitPane(){
  var center_top_pane = dijit.byId('centerTopTabPane');
//      var visit_pane  = dijit.findWidgets("centerBottomPaneTab3")
  center_top_pane.selectChild(patientHomeContentPane);
  dojo.forEach(visitHomeContentPane, function(e){e.destroyRecursive(true)})
  visitHomeContentPane.domNode.innerHTML = 
       "Please select a visit to display details here."
}


doPostDelCleanup = function (){
  //TODO
  /* This should update all the grid when a patient is deleted */
  cleanUpAdmissionPane();
  cleanUpVisitPane();
  reInitBottomPanels();
}

