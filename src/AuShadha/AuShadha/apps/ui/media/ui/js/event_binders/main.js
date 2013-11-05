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
  "dojo/parser",
  'dijit/form/FilteringSelect',
  'dijit/form/Select',

  "dojox/grid/DataGrid",
  "dojo/store/JsonRest",
  "dojo/data/ObjectStore",

  'aushadha/panes/main',
  'aushadha/panes/event_controller',
  
  'aushadha/grid/generic_grid_setup',
  'aushadha/tree/patient_tree',
  'aushadha/tree/admission_tree',
  'aushadha/tree/visit_tree',
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
           parser,

           FilteringSelect,
           Select,
           DataGrid,
           JsonRest,
           ObjectStore,
           
           auPanes,
           auPaneEventController,
           auGrids,
           auPatientTree,
           auAdmissionTree,
           auVisitTree,
           auMenu
          ){

    var auEvents={
        treeEvents: function(obj){
          return {auPatientTree   : auPatientTree, 
                  auAdmissionTree : auAdmissionTree, 
                  auVisitTree     : auVisitTree
            
          }
        },
        gridEvents: function(auGrids){
          
        },
        paneEvents: function(auPanes){
          
        },
        menuEvents: function(auMenu){
          
        },
        formEvents : function(){
                        /*
                        (function (){ // A Visit Pane Event Binder . Allow autoscrolling to the ROS section//
                            require(['dojo/window',
                                      'dojo/_base/window',
                                      'dojo/dom', 
                                      'dojo/on', 
                                      'dojo/topic'], 
                            function(win, w,dom, on){
                              on( w.body(), 
                                  'click', 
                                  function(evt){
                                    if(evt.target.id == 'visitRosAddFormTable'){
                                      evt.target.open ? win.scrollIntoView('visitRosAddFormTable'):null;
                                    }
                                  }
                              );
                            });
                        })();
                        */
        },
        getEvent : function(/*String | domId*/id, /*String | eventType*/evt){
          
        },
        setEvent: function(/*String | domId*/id, /*String | eventType*/evt){
          
        },
        startup : function(){
//                       auEvents.formEvents();
        },
        
       auPaneEventController : auPaneEventController,

       searchStores: {
         
       },

       searchApps : [],

       searchSelector : function(app){
                        var options = []
                        for (var x=0; x< auEvents.searchApps.length; x ++){
                          var d= {label: auEvents.searchApps[x].toUpperCase(), 
                                  value: auEvents.searchApps[x].toLowerCase()
                          }
                          options.push(d);
                        }
                        var searchSelector = new Select({options  : options,
                                                         name     : app+"_search_form"
                                                        },
                                                        domConstruct.create('select',
                                                                            app+'_search_form',
                                                                            'after')
                                                       );

                        searchSelector.startup();
       },

       searchWidget : function(url,placeHolder){

//                       auEvents.searchApps.push(app);
// 
//                       if (! auEvents.searchStores[app] ){
//                         auEvents.searchStores[app] = new JsonRest({target: url});
//                       }

                      var widgetStore = new JsonRest({target: url});

                        var searchBox = new FilteringSelect({regExp        : '[a-zA-Z0-9 -]+'  ,
                                                            required       : true              ,
                                                            invalidMessage : 'No Results'      ,
                                                            store          : widgetStore ,
                                                            searchAttr     : 'name'            ,
                                                            labelAttr      : 'label'           ,
                                                            labelType      : 'html'            ,
                                                            autoComplete   : false             ,
                                                            placeHolder    : placeHolder ,
                                                            hasDownArrow   : false             ,
                                                            onChange       : function(e){
                                                                                try{
                                                                                  auPaneEventController.onPatientChoice(this);
                                                                                }catch(err){
                                                                                  console.error(err.message);
                                                                                }
                                                                              },
                                                            style: "position:relative;top: 0.1em;width: 96%;height:15%;left: 2%;"
                                                            },
                                                            'search_form');
                        searchBox.startup();

        },

        headerPaneSearchWidget : function(url,placeHolder){
                            var widgetStore = new JsonRest({target: url});

                            var searchBox = new FilteringSelect({regExp        : '[a-zA-Z0-9 -]+',
                                                                required       : true,
                                                                invalidMessage : 'No Results',
                                                                store          : widgetStore,
                                                                searchAttr     : 'name',
                                                                labelAttr      : 'label',
                                                                labelType      : 'html',
                                                                autoComplete   : false,
                                                                placeHolder    : placeHolder,
                                                                hasDownArrow   : false,
                                                                onChange       : function(e){ 
                                                                                    console.log(auPaneEventController);
                                                                                    try{
                                                                                      auPaneEventController.onPatientChoice(this);
                                                                                    }catch(err){
                                                                                      console.error(err.message);
                                                                                    }
                                                                                }
                                                                },
                                                                'headerPaneSearchWidget');

                            searchBox.startup();
        }


    };

//     auEvents.startup();
    return auEvents;

});  
