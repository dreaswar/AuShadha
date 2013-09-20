define(["dijit/registry",
        "dojo/dom",
        "dojo/dom-construct",
        "dojo/dom-style",
        "dojo/_base/array",
        "dojo/ready",

        "dijit/layout/BorderContainer",
        "dojox/layout/ContentPane",
        "dijit/layout/TabContainer",

        "aushadha/panes/patient_pane",
        "aushadha/panes/admission_pane",
        "aushadha/panes/visit_pane",
        "aushadha/panes/header_pane",
//         "aushadha/panes/patient_search_pane",        
        "dojo/domReady!"
        ],
function(registry, 
        dom, 
        domConstruct, 
        domStyle, 
        array,
        ready,

        BorderContainer,
        ContentPane,
        TabContainer,

        PATIENT_PANE,
        ADMISSION_PANE,
        VISIT_PANE,
        HEADER_PANE
        ){

  var paneEventController = {

      _reInitAllPanes: function (addData){
                        console.log("Running _reInitAllPanes at panes/event_controller.js");
                        
                        this._setChosenPatient(addData);
                        this._displayPatientName(addData);

                        console.log("PATIENT_PANE variable is");
                        console.log(PATIENT_PANE);
                        PATIENT_PANE.constructor();

                        console.log("ADMISSION_PANE variable is");
                        console.log(ADMISSION_PANE);

                        ADMISSION_PANE.constructor();
                        VISIT_PANE.constructor();

//                        this._reInitAdmissionPane();
//                        this._reInitVisitPane();

                        registry.byId("centerMainPane").resize();  
      },

      _setChosenPatient : function(addData){
                          CHOSEN_PATIENT = addData;
                          console.log(CHOSEN_PATIENT);
//                           return CHOSEN_PATIENT;
      },

       _displayPatientName: function(addData){
                    domStyle.set('selected_patient_info',{"display":"",
                                                          "padding":"0px",
                                                          "margin":"0px"
                    });
                    var selectedPatientContent = addData.full_name + "-" +
                                                addData.age +"-" + addData.sex +
                                                "(" +addData.patient_hospital_id +")";
                    registry.byId('selected_patient_info').set('content', selectedPatientContent);
                    var patientInfo = dom.byId('selected_patient_info');
                    domConstruct.create("div",{ innerHTML: addData.id,
                                                id       : "selected_patient_id_info",
                                                style    : { display:"none" }
                                              },
                                              patientInfo
                    );
                    console.log( dom.byId('selected_patient_id_info').innerHTML );
      },

      _reInitAdmissionPane:function (){
                        
      },

      _reInitVisitPane: function(){
                            
      },

      onPatientChoice:function (e/* on widget obj */){
                                console.log(e.store);
                                e.store.get( e.get('value') ).
                                then(
                                  function(item /*returned item*/){
                                        console.log(item);
                                        var addData = item.addData;
                                        // This will update all Panes;
                                        paneEventController._reInitAllPanes(addData);
//                                         self.dummyFunc();
                                        console.log("Called _reInitAllPanes");
                                  }
                                );
      },

      onPatientGridSelect:function (item/* on widget obj */){
                                        console.log(item);
                                        var addData = item.addData;
                                        // This will update all Panes;
                                        paneEventController._reInitAllPanes(addData);
                                        console.log("Called _reInitAllPanes from function onPatientGridSelect ");
      },

      onPatientDelete:function (){
                    //TODO
                    /* This should update all the Panes when a patient is deleted */
      },

      _widgets: ['filteringSelectPatSearchSmall','filteringSelectPatSearch'],

      events: function(id){
                        array.forEach(this._widgets, 
                                      function(w){
                                        ready(function(){
                                          var patSearchWidget = registry.byId(w);
                                          if(patSearchWidget == true){
                                            patSearchWidget.onChange = function(e){ 
                                                                        this.onPatientChoice(e); 
                                                                      };
                                          }
                                        });
                                      });
      }
  };

  return paneEventController;

});