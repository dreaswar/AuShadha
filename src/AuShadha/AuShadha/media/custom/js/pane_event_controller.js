define(["dijit/registry",
        "dojo/dom",
        "dojo/dom-construct",
        "dojo/dom-style",
        "dojo/_base/array",

        "dijit/layout/BorderContainer",
        "dojox/layout/ContentPane",
        "dijit/layout/TabContainer",
       
      /*
        "aushadha/panes/header_pane",
        "aushadha/panes/patient_pane",
        "aushadha/panes/admission_pane",
        "aushadha/panes/visit_pane",
        "aushadha/panes/search_pane",        
      */
        ],
function(registry, 
        dom, 
        domConstruct, 
        domStyle, 
        array,
        BorderContainer,
        ContentPane,
        TabContainer
        ){

  var paneEventController = {
       
      reInitAllPanes: function (){
                        console.log("Running reInitBottomPanels at grid_setup_alt.js");

                        console.log("PATIENT_PANE variable is");
                        console.log(PATIENT_PANE);

                        PATIENT_PANE.constructor();

                        registry.byId('admissionHomeContentPane').set('disabled',false);
                        buildAdmissionTree();
                        
                        registry.byId('visitHomeContentPane').set('disabled',false);
                        buildVisitTree();

                        registry.byId("centerMainPane").resize();  
                      });
                    },


      reInitAdmissionPane:     function (){
                      var center_top_pane = dijit.byId('centerTopTabPane');
                    //      var admission_pane  = dijit.findWidgets("admissionHomeContentPane")
                      center_top_pane.selectChild(patientHomeContentPane);
                      dojo.forEach(admissionHomeContentPane, function(e){e.destroyRecursive(true)})
                      admissionHomeContentPane.domNode.innerHTML =
                          "Please select an admission to display details here."
                    },

      reInitVisitPane: function(){
                      var center_top_pane = dijit.byId('centerTopTabPane');
                    //      var visit_pane  = dijit.findWidgets("centerBottomPaneTab3")
                      center_top_pane.selectChild(patientHomeContentPane);
                      dojo.forEach(visitHomeContentPane, function(e){e.destroyRecursive(true)})
                      visitHomeContentPane.domNode.innerHTML =
                          "Please select a visit to display details here."
                    },

      doPostDelCleanup:function (){
                    //TODO
                    /* This should update all the grid when a patient is deleted */
                  }

  }
  return paneEventController;
});