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
  'aushadha/panes/event_controller'

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
           auPaneEventController){

    var auEvents={

        auPaneEventController : auPaneEventController,
 
        treeEvents: function(){
          
        },

        gridEvents: function(auGrids){
          
        },

        paneEvents: function(auPanes){
          
        },

        menuEvents: function(auMenu){
          
        },

        formEvents : function(){

        },

        getEvent : function(/*String | domId*/id, /*String | eventType*/evt){
          
        },

        setEvent: function(/*String | domId*/id, /*String | eventType*/evt){
          
        },

        startup : function(){

        },

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

                      var widgetStore = new JsonRest({target: url});
                      console.log("calling search widget function with " + url);

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
                                                                                  console.log(this);
                                                                                  auPaneEventController.onPatientChoice(this);
                                                                                }catch(err){
                                                                                  console.error(err.message);
                                                                                }
                                                                              },
                                                            style: "position:relative;top: 0.1em;width: 96%;height:15%;left: 2%;"
                                                            },
                                                            'search_form');
                        searchBox.startup();
                        console.log(searchBox);
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

    return auEvents;

});  
