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
                                {id:"familyHistoryTab"},
                                'patientSummaryTab',
                                "after"
            );
            domStyle.set('familyHistoryTab',{"height":"auto","overflow":"auto"});
                    
              domConstruct.create("div",
                                  {"id":"family_history_list_container"},
                                  'familyHistoryTab',
                                  "first"
              );
                domConstruct.create("div",
                                    {"id":"family_history_list"},
                                    'family_history_list_container',
                                    "first"
                    );
        }

        function makeDijits(){
            
            var familyHistoryTab = new ContentPane({ title     : "Family History",
                                                    closable  : true,
                                                    iconClass : "contactIcon"
                                                },
                                                "familyHistoryTab"
            );
            registry.byId('patientContextTabs').addChild(familyHistoryTab);

            setupFamilyHistoryGrid(CHOSEN_PATIENT.familyhistoryjson);

            familyHistoryTab.startup();

            registry.byId("patientContextTabs").selectChild("familyHistoryTab");
            registry.byId("patientTabsBorderContainer").resize();

        }

        function makeButtons(){
        //{% if perms.patient.add_patientfamilyhistory %}
            var addFamilyHistoryButton =  new Button({
                                          label   : "Add",
                                          title   : "Add Family History",
                                          iconClass   : "dijitIconNewTask",
                                          onClick : function(){
                                                    require(["dojo/_base/xhr", "dojo/_base/array"],
                                                    function(xhr, array){
                                                        xhr.get({
                                                                url: CHOSEN_PATIENT.familyhistoryadd,
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
                                                              id   : "addFamilyHistoryButton"
                                                              },
                                                              "family_history_list",
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