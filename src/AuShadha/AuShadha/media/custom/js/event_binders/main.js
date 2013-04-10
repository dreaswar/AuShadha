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
        auPaneEventController : auPaneEventController,

       searchWidget : function(){
                        var widgetStore = new JsonRest({target: PAT_SEARCH_JSON_URL});

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
        }
    };

    return auEvents;

});  
