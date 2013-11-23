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

        "aushadha/panes/patient_pane",
        "aushadha/panes/admission_pane",
        "aushadha/panes/visit_pane",
        "aushadha/panes/header_pane",
//      "aushadha/panes/patient_search_pane",        
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

        PATIENT_PANE,
        ADMISSION_PANE,
        VISIT_PANE,
        HEADER_PANE,
        paneAndWidgetCreator

        ){

  var paneEventController = {

      _reInitAllPanes: function (item){

                        console.log("Running _reInitAllPanes at panes/event_controller.js");
                        console.log(item[0]);

//                         query( '.mainTabContainer' ).
//                         forEach(
//                           function( i ){
//                             var tc = registry.byId( domAttr.get(i,'id') );
//                             var parentTab = tc.getParent();
//                             if ( tc.get('closable') ) {
//                                 var title = tc.get('title').toUpperCase();
//                                 window.PANES[ title ].LOAD_STATUS = false;
//                                 parentTab.removeChild( tc );
//                                 tc.destroyRecursive();
//                             }
//                         });
// 
//                         query('.subTabContainer').
//                         forEach(
//                           function(i){
//                             var tc = registry.byId( domAttr.get(i,'id') );
//                             console.log(i);
// 
//                             var children = tc.getChildren();
//                             children.forEach(function(child){
//                                 if( child.get('closable') ){
//                                   tc.removeChild(child);
//                                   child.destroyRecursive();
//                                 }
//                             });
// 
//                         });

                        var tcChildren = registry.byId('centerTopTabPane').getChildren();

                        console.log(tcChildren);

//                         tcChildren.forEach(
//                           function(i){
//                             var tc = registry.byId( domAttr.get(i,'id') );
//                             console.log(i);
// 
//                             var children = tc.getChildren();
//                             children.forEach(function(child){
//                                 if( child.get('closable') ){
//                                   tc.removeChild(child);
//                                   child.destroyRecursive();
//                                 }
//                             });
//                           }
//                         );
      
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

/*
                        this._setChosenPatient(item[0]);
                        this._displayPatientName(item[0]);
                        
                        var p = registry.byId("centerTopTabPane");
                        var c = p.getChildren();

                        console.log(c);

                        p.selectChild(c[0]);

                        c.forEach(function(i){
                            if (c.indexOf(i)>0){
                              i.set('disabled',true);
                            }
                            
                        });
*/

//                         c.forEach(
//                             function(i){ 
// //                                 console.log("Evaluating: ");
// //                                 console.log(i);
//                                 console.log(i.getChildren());
//                                 if( i.get('disabled') ){ 
//                                       i.set('disabled',false); 
//                                 }
//                         });

//                         p.selectChild( registry.byId('patient_main') );
//                         request('/AuShadha/patient/patient/summary/'+CHOSEN_PATIENT.id+'/').
//                         then(
//                           function(html){
//                             dom.byId('patient_summary_div').innerHTML = html;
//                           },
//                           function(json){
//                             var jsondata = JSON.parse(json);
//                             publishError(jsondata);
//                           },
//                           function(err){
//                             console.log(err);
//                             publishError(err);
//                             return;
//                           }
//                         );

                        registry.byId("centerMainPane").resize();                          

      },

      _setChosenPatient : function(item){
                          console.log("Resetting the Chosen Patient...");
                          CHOSEN_PATIENT = item;
                          console.log("Clearing stores...");
                          window.CHOSEN_GRID_STORE = undefined;
                          window.gridStore = {};
      },

      _displayPatientName: function(item){
                    var selectedPatientContent = item.full_name + "-" +
                                                item.age +"-" + item.sex +
                                                "(" +item.patient_hospital_id +")";

                    query('.topContentPane').
                      forEach(function(i){

                        domClass.add(i,'selected');

                        registry.
                          byId( domAttr.get(i,'id') ).
                          set( 'content', selectedPatientContent );
                    });
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

                    var p = registry.byId("centerTopTabPane");
                    var c = p.getChildren();

                    CHOSEN_PATIENT = undefined;

                    query('.topContentPane').
                      forEach(function(i){
                        domClass.remove(i,'selected');
                        registry.
                          byId( domAttr.get(i,'id') ).
                          set( 'content', '' );
                    });

                    query('.subTabContainer').
                    forEach(
                      function(i){
                        var tc = registry.byId( domAttr.get(i,'id') );
                        console.log(i);
                        var children = tc.getChildren();
                        children.forEach(function(child){
                            if( child.get('closable') ){
                              tc.removeChild(child);
                              child.destroyRecursive();
                            }
                        });
                    });

                    c.forEach(
                      function(i){ 
                          if( c.indexOf(i)>0 ){ 
                              i.set('disabled',true); 
                          }else if(c.indexOf(i)==0){
                              i.set('disabled',false); 
                              p.selectChild(i);
                          }
                    });

      }
  };

  return paneEventController;

});