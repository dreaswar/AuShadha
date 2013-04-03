define([
  'dojo/on',
  'dojo/dom',
  'dojo/dom-style',
  'dojo/dom-construct',
  'dojo/dom-geometry',
  'dojo/ready',
  'dijit/registry',
  'dojo/request',
  'dojo/json',
  
  'aushadha/panes/main',
  'aushadha/panes/event_controller',
  'aushadha/grid/grid_setup',
  'aushadha/tree/patient_tree',
  'aushadha/menu/patient_menu'
  ],
  function(on,
           dom,
           domStyle,
           domConstruct,
           domGeom,
           ready,
           registry,
           request,
           JSON,
           
           auPanes,
           auPaneEventController,
           auGrids,
           auTrees,
           auMenu
          ){

    var auEvents={
        treeEvents: function(auTrees){
          
        },
        gridEvents: function(auGrids){
          
        },
        paneEvents: function(auPanes){
          
        },
        menuEvents: function(auMenu){
          
        },
        getEvent : function(/*String | domId*/id, /*String | eventType*/evt){
          
        },
        setEvent: function(/*String | domId*/id, /*String | eventType*/evt){
          
        },
        auPaneEventController : auPaneEventController
    };
/*
    ready( function(){ 
          // Call all the Pane event binders. 
           auPaneEventController.events(); 
    }); 
*/
    return auEvents;

});  
