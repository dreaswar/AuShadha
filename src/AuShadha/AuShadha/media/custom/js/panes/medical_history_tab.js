define([
        "dojo/dom",
        'dojo/dom-class',
        'dojo/dom-style',
        'dojo/dom-construct',
        'dojo/on',

        'dijit/registry',
        'dijit/layout/BorderContainer',
        'dojox/layout/ContentPane',
        'dijit/layout/TabContainer',
        'dijit/form/Button',
        "dijit/Dialog",
        "dojo/request",
        "dojo/json",

       'aushadha/grid/grid_structures',
       'aushadha/grid/grid_setup',

        "dojo/domReady!",
    ],
    function(dom,
             domClass,
             domStyle,
             domConstruct,
             on,
             registry,
             BorderContainer,
             ContentPane,
             TabContainer,
             Button,
             Dialog,
             request,
             JSON,

             GRID_STRUCTURES,
             auGridSetup
    ){

          function createHistoryDoms(){
              domConstruct.create('div',
                                      {id: "patientMedicalHistoryTab"},
                                      "patientContextTabs",
                                      "last"
                  );

              domConstruct.create('div',
                                  {id: "medical_history_list"},
                                  "patientMedicalHistoryTab",
                                  "first"
              );
          }

          function createHistoryDijits(){
            //{% if perms.medical_history %}
              if(registry.byId('patientMedicalHistoryTab')){
                registry.byId('patientMedicalHistoryTab').destroyRecursive(true);
              }
                var medicalHistoryTab = new ContentPane({id      : "patientMedicalHistoryTab",
                                                        title    : "Medical History",
                                                        closable : true
                                                  },
                                                  "patientMedicalHistoryTab"
                                                  );
                registry.byId("patientContextTabs").addChild(medicalHistoryTab);

              //{% endif %}
          }

          function createButtons(){
                //{% if perms.medical_history.add_medicalhistory %}
                    var addPatientMedicalHistoryButton =  new Button({
                                                          label       : "Add",
                                                          title       : "Add Medical History Details",
                                                          iconClass   : "dijitIconNewTask",
                                                          onClick: function(){
                                                                require(
                                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                                  function(xhr, array){
                                                                    xhr.get({
                                                                      url: CHOSEN_PATIENT.medicalhistoryadd,
                                                                      load: function(html){
                                                                                var myDialog = dijit.byId("editPatientDialog");
                                                                                myDialog.set('content', html);
                                                                                myDialog.set('title', "Record New Medical History Details");
                                                                                myDialog.show();
                                                                            }
                                                                  });
                                                                })
                                                          }
                                        },
                                        domConstruct.create('button',
                                                            {type : "button",
                                                            id   : "addPatientMedicalHistoryButton"
                                                            },
                                                            "medical_history_list",
                                                            "before"
                                        )
                );
                //{% endif %}
          }

          function fillData(){
            //{% if perms.medical_history %}
              var medicalHistoryUrl   = CHOSEN_PATIENT.medicalhistoryjson;
              console.log(auGridSetup);
              auGridSetup.setupMedicalHistoryGrid(medicalHistoryUrl);
              registry.byId("patientContextTabs").selectChild('patientMedicalHistoryTab');
            //{% endif %}
          }

          return {
            constructor: function(){
                              createHistoryDoms();
                              createHistoryDijits();
                              createButtons();
                              fillData();
                          }
          }
    });