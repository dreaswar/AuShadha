/* Sets up all the Data Grids for FDA Drug DB */

define(["dojo/dom",
        "dojo/dom-attr",
        "dojox/grid/DataGrid",
        "dojo/store/JsonRest",
        "dojo/data/ObjectStore",
        "dijit/registry",
        "dojox/layout/ContentPane",
        "dijit/Dialog",
        "dojo/_base/xhr",
        "dojo/_base/lang",
        'dojo/request',
        'dojo/json',
        "aushadha/stores",
        "aushadha/grid/grid_structures",
        "aushadha/panes/event_controller",
        'aushadha/panes/dynamic_html_pane_creator',
        "dojo/domReady!"
  ],
  function (dom,
            domAttr,
            DataGrid,
            JsonRest,
            ObjectStore,
            registry,
            ContentPane,
            Dialog,
            xhr,
            lang,
            request,
            JSON,

            aushadhaStores,
            GRID_STRUCTURES,
            auEventController,
            createDynamicHTMLPane) {

      var onGridRowClick= function ( e,gridToUse /*click_event, grid_obj*/) {

          var idx = e.rowIndex,
              item = gridToUse.getItem(idx);
          var url = gridToUse.store.getValue(item,'url');
          var updateDom = gridToUse.store.getValue(item,'updateDom')? gridToUse.store.getValue(item,'updateDom'):'FDA_DRUG_SUMMARY_CP';
          var id = gridToUse.store.getValue(item, "id");
          gridToUse.selection.clear();
          gridToUse.selection.setSelected(item, true);

          request(url).then(
            function(html){
                window.CHOSEN_GRID = domAttr.get(gridToUse.domNode,'id');
                registry.byId(updateDom).set('href',url);
            },
            function(json){
              publishError(json);
              return false;
            },
            function(err){
              console.log(err);
              publishError(err);
            });

          return false;
      }


      var setupGrid =     function (args) {
          
            require( [args.gridStrModule], 
            function(gridStr){ 

                var Str = gridStr[args.str];

                var gridUrl = args.url,
                    gridDomNode = args.gridDomNode,
                    gridName = args.gridName,
                    storeToUse = args.storeToUse,
                    activateRowClick = args.activateRowClick? args.activateRowClick:true;

                
                console.log(Str);
                   
                if (!window.gridStore[storeToUse]){
                    console.log("No store set for : " + storeToUse );
                    console.log("Creating the same...");
                    window.gridStore[storeToUse] = new JsonRest({target: gridUrl,
                                                      idProperty: 'id'
                                                    });
                }

                var grid = new DataGrid({
                        store: dataStore = ObjectStore({
                            objectStore: window.gridStore[storeToUse]
                        }),
                        /*,
                        query: {
                            search_field: 'id',
                            search_for: "*"
                        },
                        */
                        clientSort: true,
                        autoWidth: true,
                        selectionMode: "single",
                        rowSelector: "20px",
                        structure: Str,
                        noDataMessage: "<span class='dojoxGridNoData'>No Matching Data</span>"
                    },
                    gridDomNode
                );
                grid.activateRowClick = activateRowClick;
                grid.title = gridName ? gridName.toString():"FDA Drugs";
                grid.canSort = function () {
                    return true;
                };

                grid.onRowClick = function (e) {
                    /*
                      Get the Clicked Rows index and the Grid item 
                    */

//                     var idx = e.rowIndex,
//                         item = this.getItem(idx);
//                     grid.selection.clear();
//                     grid.selection.setSelected(item, true);

                     if (grid.activateRowClick) {
                       onGridRowClick(e,grid);
                     }
                     else{ 
                      return false; 
                     }

                }

                grid.startup();                
                console.log(grid);
                return grid;
              });
           }

      return setupGrid;

});
