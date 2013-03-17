function createSurgicalHistoryTab(){
    require([
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
            "dojo/domReady!"
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
             JSON
    ){

          function createHistoryDoms(){
              domConstruct.create('div',
                                      {id: "patientSurgicalHistoryTab"},
                                      "patientSummaryTab",
                                      "after"
                  );

              domConstruct.create('div',
                                  {id: "surgical_history_list"},
                                  "patientSurgicalHistoryTab",
                                  "first"
              );
          }

          function createHistoryDijits(){
            //{% if perms.patient %}
              if(registry.byId('patientSurgicalHistoryTab')){
                registry.byId('patientSurgicalHistoryTab').destroyRecursive(true);
              }
                var surgicalHistoryTab = new ContentPane({id      : "patientSurgicalHistoryTab",
                                                        title    : "Surgical History",
                                                        closable : true
                                                  },
                                                  "patientSurgicalHistoryTab"
                                                  );
                registry.byId("patientContextTabs").addChild(surgicalHistoryTab);

              //{% endif %}
          }

          function createButtons(){
                //{% if perms.patient.add_patientsurgicalhistory %}
                    var addPatientsurgicalHistoryButton =  new Button({
                                                          label       : "Add",
                                                          title       : "Add Surgical History",
                                                          iconClass   : "dijitIconNewTask",
                                                          onClick: function(){
                                                                require(
                                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                                  function(xhr, array){
                                                                    xhr.get({
                                                                      url: CHOSEN_PATIENT.surgicalhistoryadd,
                                                                      load: function(html){
                                                                                var myDialog = dijit.byId("editPatientDialog");
                                                                                myDialog.set('content', html);
                                                                                myDialog.set('title', "Record New Surgical History Details");
                                                                                myDialog.show();
                                                                            }
                                                                  });
                                                                })
                                                          }
                                        },
                                        domConstruct.create('button',
                                                            {type : "button",
                                                            id   : "addPatientSurgicalHistoryButton"
                                                            },
                                                            "surgical_history_list",
                                                            "before"
                                        )
                );
                //{% endif %}
          }

          function fillData(){
            //{% if perms.patient %}
              var surgicalHistoryUrl   = CHOSEN_PATIENT.surgicalhistoryjson;
              setupSurgicalHistoryGrid(surgicalHistoryUrl);
              registry.byId("patientContextTabs").selectChild('patientSurgicalHistoryTab');
            //{% endif %}
          }

           createHistoryDoms();
           createHistoryDijits();
           createButtons();
           fillData();

    });
}
