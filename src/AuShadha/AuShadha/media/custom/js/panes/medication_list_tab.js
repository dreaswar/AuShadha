function (urlObj/* URL DICT */){
    require([
            "dojo/dom",
            "dojo/dom-style",
            "dojo/query",
            "dojo/dom-construct",

            "dijit/registry",
            "dijit/form/Button",
            "dojox/layout/ContentPane",
            "dijit/layout/TabContainer",
            "dijit/layout/BorderContainer",
    ], 
    function(dom, 
             domStyle,
             query,
            domConstruct, 
            registry, 
            Button,
            ContentPane, 
            TabContainer, 
            BorderContainer){

        function makeDoms(){
            domConstruct.create('div',
                                {id:"medicationListTab"},
                                'patientSummaryTab',
                                "after"
            );
            domStyle.set('medicationListTab',{"height":"auto","overflow":"auto"});
            
            domConstruct.create("div",
                                {"id":"medication_list_container"},
                                'medicationListTab',
                                "first"
            );
              domConstruct.create("div",
                                  {"id":"medication_list"},
                                  'medication_list_container',
                                  "first"
                  );
            
              domConstruct.create('div',
                                  {id: "patient_allergy_div"},
                                  "medication_list",
                                  "after"
              );
              domStyle.set( dom.byId('patient_allergy_div'),
                                          { "height"   : '25em',
                                            "position" : "relative",
                                            "top"      : "-25.5em",
                                            "left"     : "58em",
                                            "width"    : "25em"
              });
                domConstruct.create('div',
                                    {id: "patient_allergyHeader"},
                                    "patient_allergy_div",
                                    "first"
                );
                  domStyle.set( dom.byId('patient_allergyHeader'),
                                          {"width"         : "25em",
                                          'height'         : "auto"  ,
                                          "display"        : "block" ,
                                          "float"          : "left"  ,
                                          "clear"          : "both" ,
                                          "position"       : "relative",
                                          "top"            : "0"        ,
                                          "padding"        : "1px",
                                          "background"     : "#2D285A",
                                          "color"          : "whitesmoke",
                                          "textAlign"      : "center",
                                          "verticalAlign"  : "middle",
                                          "fontWeight"     : "bold",
                                          "fontFamily"     : "dejavu sans"
                      });
                  dom.byId("patient_allergyHeader").innerHTML = "ALLERGY";
                domConstruct.create('div',
                                    {id: "patient_allergyGridContainer"},
                                    "patient_allergyHeader",
                                    "after"
                );
                  domStyle.set( dom.byId('patient_allergyGridContainer'),
                                            {'height'        : "auto"      ,
                                             "width"         : "25em"      ,
                                            "display"        : "block"     ,
                                            "float"          : "left"      ,
                                            "clear"          : "both"      ,
                                            "position"       : "relative"  ,
                                            "top"            : "0em"     ,
                                            "fontFamily"     : "dejavu sans"
                  });
                domConstruct.create('div',
                                      {id: "allergy_list"},
                                      "patient_allergyGridContainer",
                                      "first"
                );
                domStyle.set('allergy_list' , {height: '21.5em', width: "25em"});

        }

        function makeDijits(){
            
            var medicationListTab = new ContentPane({ title     : "Medication List",
                                                    closable  : true,
                                                    iconClass : "contactIcon"
                                                },
                                                "medicationListTab"
            );
            registry.byId('patientContextTabs').addChild(medicationListTab);

            setupMedicationListGrid(CHOSEN_PATIENT.medicationlistjson);
            setupAllergiesGrid(CHOSEN_PATIENT.allergiesjson);

            medicationListTab.startup();

            registry.byId("patientContextTabs").selectChild("medicationListTab");
            registry.byId("patientTabsBorderContainer").resize();

        }

        function makeButtons(){
        //{% if perms.patient.add_patientmedicationlist %}
            var addMedicationListButton =  new Button({
                                          label   : "Add",
                                          title   : "Add Family History",
                                          iconClass   : "dijitIconNewTask",
                                          onClick : function(){
                                                    require(["dojo/_base/xhr", "dojo/_base/array"],
                                                    function(xhr, array){
                                                        xhr.get({
                                                                url: CHOSEN_PATIENT.medicationlistadd,
                                                                load: function(html){
                                                                              var myDialog = dijit.byId("editPatientDialog");
                                                                              myDialog.set('content', html);
                                                                              myDialog.set('title', "Add Family History");
                                                                              myDialog.show();
                                                                      }
                                                        });
                                                    });
                                                  }
                                          },
                                          domConstruct.create('button',
                                                              {type : "button",
                                                              id   : "addMedicationListButton"
                                                              },
                                                              "medication_list",
                                                              "before"
                                          )
                                        );
        //{% endif %}
        
        //{% if perms.patient.add_patientallergies %}
            var addMedicationListButton =  new Button({
                                          label   : "Add",
                                          title   : "Add Allergy",
                                          iconClass   : "dijitIconNewTask",
                                          onClick : function(){
                                                    require(["dojo/_base/xhr", "dojo/_base/array"],
                                                    function(xhr, array){
                                                        xhr.get({
                                                                url: CHOSEN_PATIENT.allergiesadd,
                                                                load: function(html){
                                                                              var myDialog = dijit.byId("editPatientDialog");
                                                                              myDialog.set('content', html);
                                                                              myDialog.set('title', "Add Allergy");
                                                                              myDialog.show();
                                                                      }
                                                        });
                                                    });
                                                  }
                                          },
                                          domConstruct.create('button',
                                                              {type : "button",
                                                              id   : "addAllergyButton"
                                                              },
                                                              "allergy_list",
                                                              "before"
                                          )
                                        );
        //{% endif %}

        }

    makeDoms();
    makeDijits();
    makeButtons();

    });


}