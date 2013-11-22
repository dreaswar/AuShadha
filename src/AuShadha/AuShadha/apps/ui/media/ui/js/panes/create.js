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
       'aushadha/tree/generic_tree_builder',
       'aushadha/panes/create_main_pane',
       'aushadha/panes/create_sub_module_pane',
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
        buildGenericTree,
        createMainModulePane,
        createSubModulePane,
        testPaneCreator,

        ready){


      var pane = {

        panes: [],

        constructor: function() {

              var appObj = window.INSTALLED_APPS ? window.INSTALLED_APPS: [];

              console.log( appObj );

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

              if ( window.DEFERRED_LOAD_PANES.length >0 ) {

                for( var x=0; x< window.DEFERRED_LOAD_PANES.length; x++ ) {

                  appPaneCreator( window.DEFERRED_LOAD_PANES[x] );
                  window.DEFERRED_LOAD_PANES.shift();

                }

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

        window.PANES[ title.toUpperCase() ] = { LOAD_STATUS : false }

        function runMainModulePaneCreator(){

//           if ( window.PANES[loadAfter.toUpperCase()].LOAD_STATUS  || loadAfter == 'first' ){

          if ( loadFirst == true ){


              if (title == 'Search' ){

                if ( uiSections.widgets.pane ){

                  request(uiSections.widgets.pane).then(
                    function(json){
                      var jsondata  = JSON.parse(json);
                      testPaneCreator.constructor(jsondata.pane);
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

//               var mainTabPaneDomNode = createMainModulePane( d, p, title, domId );
// 
//               if ( url ) {
// 
//                 var domN = domId+"_leading_tree";
//                 console.log(buildGenericTree);
//                 buildGenericTree( url, domN, mainTabPaneDomNode );
// 
//               }
// 
//               if ( gridEnabled ){
// 
//                 console.log("Grid Store URL is : " + gridEnabled);
// 
//                 var gridTitle = title.replace(' ','_'); 
//                 gridTitle = gridTitle.toUpperCase().toString();
// 
//                 var gridStore = gridTitle + "_GRID_STORE";
//                 var gridDom   = gridTitle.toLowerCase()+"_grid_container";
// 
//                 console.log("Trying to Grid for App : , " + gridTitle + 
//                             " with Store as: " + gridStore + 
//                             " and DOM as " + gridDom
//                            );
// 
//                 if (! dom.byId('search_grid_tc') ){
// 
//                   domConstruct.create('div',
//                                       { id    : 'search_grid_tc'},
//                                       'search_cp_grid',
//                                       0
//                                     );
//                 }
// 
//                 if (! registry.byId('search_grid_tc') ) {
// 
//                   var search_tc = new TabContainer({id:'search_grid_tc',
//                                                     tabPosition:'top',
//                                                     tabStrip:true
//                                                   });
// 
//                   registry.byId('search_cp_grid').addChild(search_tc);
// 
//                 }
// 
//                 else{
//                   var search_tc  = registry.byId('search_grid_tc');
//                 }
// 
//                 if (! dom.byId(gridDom) ) {
// 
//                   domConstruct.create('div',
//                                       { id    : gridDom+"_grid_cp"},
//                                       'search_grid_tc',
//                                       'last'
//                                     );
// 
//                   domConstruct.create('div',
//                                       { id    : gridDom,
//                                         class : 'gridContainer'
//                                       },
//                                       gridDom+"_grid_cp",
//                                       'last'
//                                     );
// 
//                 }
// 
//                 if ( ! registry.byId( gridDom+"_grid_cp") ) {
// 
//                   cp = new ContentPane({id: gridDom+"_grid_cp",
//                                         title: title },
//                                         gridDom+"_grid_cp"
//                                       );
// 
//                   search_tc.addChild(cp);
// 
//                 }
// 
//                 search_tc.startup();
// 
//                 auGenericGridSetup.setupGrid(
//                                             gridEnabled,                   // URL of the GRID
//                                             gridDom,                       // DOM id to put the Grid into
//                                             GRID_STRUCTURES[gridTitle],    // Grid Structure
//                                             true,                          // Whether to activate RowSingleClick behavior
//                                             gridTitle,                     // Title of the Grid
//                                             gridStore                      // Variable name for Grid Store
//                                             );
// 
//               }

//               if ( searchEnabled ) {
//                 console.log("Enabling Search for Header Pane Search widget with URL of : " + searchEnabled );
//                 auMain.auEventBinders.headerPaneSearchWidget( searchEnabled,'Search for:  '+ title);
//                 auMain.auEventBinders.searchWidget( searchEnabled,'Search for:  '+ title);                    
// 
//               }                        

              window.PANES[ title.toUpperCase() ].LOAD_STATUS = true;

          }

          else{
            window.DEFERRED_LOAD_PANES.push( obj[x] );
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