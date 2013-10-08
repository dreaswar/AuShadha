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

  "dojox/grid/DataGrid",
  "dojo/store/JsonRest",
  "dojo/data/ObjectStore",

  'aushadha/panes/main',
  'aushadha/panes/event_controller',
  'aushadha/grid/grid_setup',
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

       searchWidget : function(){
                        var widgetStore = new JsonRest({target: PAT_SEARCH_JSON_URL?PAT_SEARCH_JSON_URL:''});

                        var searchBox = new FilteringSelect({regExp        : '[a-zA-Z0-9 -]+'  ,
                                                            required       : true              ,
                                                            invalidMessage : 'No Results'      ,
                                                            store          : widgetStore       ,
                                                            searchAttr     : 'name'            ,
                                                            labelAttr      : 'label'           ,
                                                            labelType      : 'html'            ,
                                                            autoComplete   : false             ,
                                                            placeHolder    : 'Patient\'s Name' ,
                                                            hasDownArrow   : false             ,
                                                            onChange       : function(e){
                                                                                try{
                                                                                  auPaneEventController.onPatientChoice(this);
                                                                                }catch(err){
                                                                                  console.error(err.message);
                                                                                }
                                                                              },
                                                            style          : 'width:160%; textAlign:center;'
                                                            },
                                                            'filteringSelectPatSearch');

                        searchBox.startup();
        },

        headerPaneSearchWidget : function(){
                            var widgetStore = new JsonRest({target: PAT_SEARCH_JSON_URL?PAT_SEARCH_JSON_URL:''});

                            /*
                            domStyle.set('filteringSelectPatSearchSmall',
                                         {width      : '250px',
                                          height     : '18px',
                                          margin     : 'none',
                                          padding    : 'none',
                                          position   : 'relative',
                                          top        : '-3.0em',
                                          marginLeft : '10px'
                            });
                            */

                            var searchBox = new FilteringSelect({regExp        : '[a-zA-Z0-9 -]+',
                                                                required       : true,
                                                                invalidMessage : 'No Results',
                                                                store          : widgetStore,
                                                                searchAttr     : 'name',
                                                                labelAttr      : 'label',
                                                                labelType      : 'html',
                                                                autoComplete   : false,
                                                                placeHolder    : 'Patient\'s Name',
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
                                                                'filteringSelectPatSearchSmall');

                            searchBox.startup();
        }

    };

//     auEvents.startup();
    return auEvents;

});  
