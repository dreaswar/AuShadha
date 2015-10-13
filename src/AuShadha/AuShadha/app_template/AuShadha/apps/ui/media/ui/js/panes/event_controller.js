define(["dijit/registry",
        "dojo/dom",
        "dojo/dom-construct",
        "dojo/dom-style",
        'dojo/dom-class',
        'dojo/dom-attr',
        "dojo/_base/array",
        "dojo/ready",
        'dojo/query',
        'dojo/request',
        'dojo/json',

        "dijit/layout/BorderContainer",
        "dojox/layout/ContentPane",
        "dijit/layout/TabContainer",

        "aushadha/under_construction/pane_and_widget_creator",

        "dojo/domReady!"
        ],

  function(registry, 
        dom, 
        domConstruct, 
        domStyle, 
        domClass,
        domAttr,
        array,
        ready,
        query,
        request,
        JSON,

        BorderContainer,
        ContentPane,
        TabContainer,

        paneAndWidgetCreator

        ){

  var paneEventController = {

      _reInitAllPanes: function (item){

                        console.log("Running _reInitAllPanes at panes/event_controller.js");

                        this.clearLoadedTabs();
                        this._setChosenPatientAndGridStore(item[0]);

                        request( item[0].paneUrl ).
                        then(

                          function(json){
                            var jsondata = JSON.parse(json);
                            paneAndWidgetCreator.constructor(jsondata.pane)
                          },

                          function(json){
                            var jsondata = JSON.parse(json);
                            publishError(jsondata.error_message);
                          }

                        );

                        registry.byId("centerMainPane").resize();                          

      },

      clearLoadedTabs: function (){
        var p = registry.byId("centerTopTabPane");
        var c = p.getChildren();

        if ( c.length > 1 ) {
          c.forEach(function(i){
            if (c.indexOf(i)>0){
              p.removeChild(i);
              i.destroyRecursive();
            }
          });
        }

        p.selectChild(c[0]);

      },

      _setChosenPatientAndGridStore : function(item){
                          console.log("Resetting the Chosen Patient...");
                          CHOSEN_PATIENT = item;
                          console.log("Clearing stores...");
                          window.CHOSEN_GRID_STORE = undefined;
                          window.gridStore = {};
      },

      _resetChosenPatientAndGridStore : function(){
                          console.log("Resetting the Chosen Patient...");
                          CHOSEN_PATIENT = undefined;
                          console.log("Clearing stores...");
                          window.CHOSEN_GRID_STORE = undefined;
                          window.gridStore = {};
      },

      _reInitAdmissionPane:function (){
                        
      },

      _reInitVisitPane: function(){
                            
      },

      onPatientChoice:function (e/* on widget obj */){
//                                 console.log(e.store);
                                e.store.get( e.get('value') ).
                                then(
                                  function(item /*returned item*/){
//                                         console.log(item);
                                        // This will update all Panes;
                                        paneEventController._reInitAllPanes(item);
                                        console.log("Called _reInitAllPanes");
                                  }
                                );
      },

      onPatientGridSelect:function (item/* on widget obj */){
//                                         console.log(item);
                                        // This will update all Panes;
                                        paneEventController._reInitAllPanes(item);
                                        console.log("Called _reInitAllPanes from function onPatientGridSelect ");
      },

      onPatientDelete:function (){
        this._resetChosenPatientAndGridStore();
        this.clearLoadedTabs();
      }

  };

  return paneEventController;

});