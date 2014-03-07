// The module loader for AuShadha scripts
define(['dojo/dom',
        'dojo/dom-construct',
        'dojo/dom-style',
        'dojo/on',
        'dojo/json',
        'dojo/_base/array',
        'dijit/registry',
        'dijit/layout/BorderContainer',
        'dojox/layout/ContentPane',
        'dijit/layout/TabContainer',
        'dijit/form/FilteringSelect',

        "dojo/parser",

        "dojox/grid/DataGrid",
        "dojo/store/JsonRest",
        "dojo/data/ObjectStore",
        "dojo/request",
        "dojo/json",

       "aushadha/main",
       "aushadha/grid/generic_grid_setup",
       "aushadha/grid/grid_structures",
       "aushadha/under_construction/pane_and_widget_creator",

       "dojo/ready",
       'dojo/domReady!'
    ],
    function (dom,
        domConstruct,
        domStyle,
        on,
        JSON,
        array,
        registry,
        BorderContainer,
        ContentPane,
        TabContainer,
        FilteringSelect,

        parser,
        DataGrid,
        JsonRest,
        ObjectStore,
        request,
        JSON,
       
        auMain,
        auGenericGridSetup,
        GRID_STRUCTURES,
        paneAndWidgetCreator,

        ready){


      var pane = {

        panes: [],

        constructor: function() {

              var appObj = window.INSTALLED_APPS ? window.INSTALLED_APPS: [];

//               console.log( appObj );

              var centerMainPane = registry.byId('centerMainPane');
              var centerTopTabPane= registry.byId("centerTopTabPane");

              if ( !centerTopTabPane ) {

                if (! dom.byId('centerTopTabPane') ) {

                  domConstruct.create('div',
                                      {id:'centerTopTabPane'},
                                      'centerMainPane',0
                                     );

                }

                centerTopTabPane = new TabContainer({ tabPosition:'top',
                                                      tabStrip:true
                                                    },
                                                    'centerTopTabPane'
                                                   );

                centerMainPane.addChild( centerTopTabPane );
                centerTopTabPane.startup();

              }

              for ( var x=0; x < appObj.length; x++ ) {

                appPaneCreator( appObj[x] );
                console.log("Created " + appObj[x].app + " Pane");
              }

              if ( centerTopTabPane.hasChildren() ) {

                centerTopTabPane.selectChild( centerTopTabPane.getChildren()[0] );

              }

        },

        destroyPane: function(){
          for( var x = 0; x < pane.panes.length; x++ ) {
            registry.byId( pane.panes[x].domNode ).destroyRecursive();
          }
        }

      }

      function appPaneCreator( appObj ) {

        var title = appObj.app;
        var url = appObj.url;
        var domId = appObj.app.replace(' ','_').toLowerCase();
        var uiSections = appObj.ui_sections;            

        var layoutSections = uiSections.layout;
        var appType = uiSections.app_type;

        var loadFirst = uiSections.load_first;
        var loadAfter = uiSections.load_after;

        var gridEnabled = uiSections.widgets.grid;
        var searchEnabled = uiSections.widgets.search;
        var treeEnabled = uiSections.widgets.tree;
        var summaryEnabled = uiSections.widgets.summary;

        var d = dom.byId(domId);
        var p = registry.byId(domId);

        console.log("Creating pane with domId: " + domId);

        // This Basically parses the json.pane from the AuShadha/apps/search/views's render_search_pane and creates a search UI with 
        // search forms, widgets etc..
        function runMainModulePaneCreator(){

          if ( loadFirst == true ){

              if (title == 'Search' ){

                if ( uiSections.widgets.pane ){

                  request(uiSections.widgets.pane).then(
                    function(json){
                      var jsondata  = JSON.parse(json);
                      paneAndWidgetCreator.constructor(jsondata.pane);
                      auMain.auEventBinders.headerPaneSearchWidget( searchEnabled,'Search for:  '+ title);
                      if ( dom.byId('search_form') ){
                        auMain.auEventBinders.searchWidget( searchEnabled,'Search for:  '+ title);
                      }
                      else{
                        alert("Dom is not ready for searching");
                      }
                    }
                  );

                }

              }

          }

        }

        if ( appType == 'main_module' && loadFirst == true ){
          runMainModulePaneCreator();
        }

//         else if( appType == 'main_module' && loadFirst == false ){
//           runMainModulePaneCreator();
//         }

//         else if( appType == 'sub_module' ){
//           createSubModulePane( d,p,title,domId );
//         }

    }

    return pane.constructor ;

});
