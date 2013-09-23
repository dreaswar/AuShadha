define([
      "dojo/dom",
      "dojo/dom-style",
      "dojo/query",
      "dojo/dom-construct",

      "dijit/registry",
      "dijit/form/Button",
      "dojox/layout/ContentPane",
      "dijit/layout/TabContainer",
      "dijit/layout/BorderContainer",
      
      'aushadha/grid/grid_structures',
      'aushadha/grid/grid_setup'
    ], 
    function(dom, 
             domStyle,
             query,
             domConstruct, 
             registry, 
             Button,
             ContentPane, 
             TabContainer, 
             BorderContainer,

             GRID_STRUCTURES,
             auGridSetup
            ){

        function makeDoms(){
            domConstruct.create('div',
                                {id:"immunisationTab"},
                                'patientSummaryTab',
                                "after"
            );
            domStyle.set('immunisationTab',{"height":"auto","overflow":"auto"});
            
            domConstruct.create("div",
                                {"id":"immunisation_container"},
                                'immunisationTab',
                                "first"
            );
              domConstruct.create("div",
                                  {"id":"immunisation_list"},
                                  'immunisation_container',
                                  "first"
                  );


        }

        function makeDijits(){
            
            var immunisationTab = new ContentPane({ title     : "Immunisations",
                                                    closable  : true,
                                                    iconClass : "contactIcon"
                                                },
                                                "immunisationTab"
            );
            registry.byId('patientContextTabs').addChild(immunisationTab);

            auGridSetup.setupImmunisationGrid(CHOSEN_PATIENT.immunisationjson);

            immunisationTab.startup();

            registry.byId("patientContextTabs").selectChild("immunisationTab");
            registry.byId("patientTabsBorderContainer").resize();

        }

        function makeButtons(){
        //{% if perms.immunisation.add_immunisation %}
            var addImmunisationButton =  new Button({
                                          label   : "Add",
                                          title   : "Add Immunisation",
                                          iconClass   : "dijitIconNewTask",
                                          onClick : function(){
                                                    require(["dojo/_base/xhr", "dojo/_base/array"],
                                                    function(xhr, array){
                                                        xhr.get({
                                                                url: CHOSEN_PATIENT.immunisationadd,
                                                                load: function(html){
                                                                              var myDialog = dijit.byId("editPatientDialog");
                                                                              myDialog.set('content', html);
                                                                              myDialog.set('title', "Add Immunisation");
                                                                              myDialog.show();
                                                                      }
                                                        });
                                                    });
                                                  }
                                          },
                                          domConstruct.create('button',
                                                              {type : "button",
                                                              id   : "addImmunisationButton"
                                                              },
                                                              "immunisation_list",
                                                              "before"
                                          )
                                        );
        //{% endif %}
        }

    return {
     constructor: function(){
                      makeDoms();
                      makeDijits();
                      makeButtons();
                  }
    }

});