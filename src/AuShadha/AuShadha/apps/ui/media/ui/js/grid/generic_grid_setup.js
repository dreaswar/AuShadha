/* Sets up all the Data Grids. 
 * this can be refactored
 * right now I have left it with repetitive code for each grid
 * a common function should be enough to generate all the grids
 */

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

      var onGridRowDblClick= function ( obj/*e, gridToUse, titleToUse*/) {

          var gridToUse = obj.grid;
          var e = obj.event;
          var titleToUse = obj.title;
          var gridId = obj.gridId;

          var idx = e.rowIndex,
              item = gridToUse.getItem(idx);

          var id = gridToUse.store.getValue(item, "id");
          var edit = gridToUse.store.getValue(item, "edit");
          var del = gridToUse.store.getValue(item, "del");

          gridToUse.selection.clear();
          gridToUse.selection.setSelected(item, true);

          request(edit).then(
            function(html){

                var myDialog = registry.byId("editPatientDialog");

                window.CHOSEN_GRID = domAttr.get(gridToUse.domNode,'id');

                if (myDialog == undefined || myDialog == null) {
                    myDialog = new Dialog({
                                          title: titleToUse,
                                          content: html,
                                          style: "width: 500px; height:500px;"
                                      },
                                      "editPatientDialog"
                                  );
                    myDialog.startup();
                }
                else{
                    myDialog.set('content', html);
                    myDialog.set('title', titleToUse);
                }
                myDialog.show();
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

      return {

          setupPopUpGrid: function (url, gridStr, divId) {

                var Cstore = new JsonRest({
                    target: url
                });
                console.log(Cstore);
                console.log("Creating the Popup Grid")

                if (registry.byId(divId)) {
                    registry.byId(divId)
                        .destroyRecursive(true);
                }

                var popUpGrid = new DataGrid({
                        store: dataStore = ObjectStore({
                            objectStore: Cstore
                        }),
                        selectionMode: "single",
                        rowSelector: "20px",
                        structure: gridStr,
                        noDataMessage: "<span class='dojoxGridNoData'>No Information in Store..</span>",
                        style: "height: 600px; width: 600px; overflow:auto; "
                    },
                    divId
                );

                popUpGrid.onRowDblClick = function (e) {
                      var args = {event: e,grid: popUpGrid, title: "Edit Contact"};
                      var toCall = lang.hitch(this,onGridRowDblClick,args);
                      toCall();
                    return false;
                };
                popUpGrid.startup();
                console.log("Finished creating Pop-up Grid");
          },

           setupGrid: function (gridUrl, gridDomNode, gridStr, activateRowClick, gridName, storeToUse) {
                
//                 console.log("URL: " + gridUrl + "\nDOM: " + gridDomNode + "\nSTR: " );
//                 console.log( gridStr );
//                 debugger;

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
                        /*
                        query: {
                            search_field: 'id',
                            search_for: "*"
                        },
                        */
                        query: {id: '*'}, 
                        rowsPerPage: 25,
                        keepRows: 75, 
                        clientSort: true,
                        autoWidth: true,
                        selectionMode: "single",
                        rowSelector: "20px",
                        structure: gridStr,
                        noDataMessage: "<span class='dojoxGridNoData'>No Matching Data</span>"
                    },
                    gridDomNode
                );

                grid.activateRowClick = activateRowClick;

                grid.title = gridName ? gridName.toString():"Patient";

                grid.canSort = function () {
                    return true;
                };

                grid.onRowClick = function (e) {
                    /*
                      Get the Clicked Rows index and the Grid item 
                    */
                    var idx = e.rowIndex,
                        item = this.getItem(idx);
                    grid.selection.clear();
                    grid.selection.setSelected(item, true);

                    if (grid.activateRowClick) {
                      auEventController.onPatientGridSelect(item);
                    }
                    else{ 
                      return false; 
                    }

                }

                grid.onRowDblClick = function(e){ 
                                        onGridRowDblClick({event: e, 
                                                           grid: grid, 
                                                           title: grid.title,
                                                           gridId : gridDomNode
                                                          });
                }

                grid.startup();                
                console.log(grid);
                return grid;
            },

            setupDynamicPaneGrid: function (gridUrl, gridDomNode, gridStr, activateRowClick, gridName, storeToUse) {

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
                        structure: gridStr,
                        noDataMessage: "<span class='dojoxGridNoData'>No Matching Data</span>"
                    },
                    gridDomNode
                );

                grid.activateRowClick = activateRowClick;

                grid.title = gridName ? gridName.toString():"Patient";

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

//                     if (grid.activateRowClick) {
//                       auEventController.onPatientGridSelect(item);
//                     }
//                     else{ 
                      return false; 
//                     }

                }

                grid.onRowDblClick = function(e){ 
                                                var idx = e.rowIndex,
                                                    item = this.getItem(idx);
                                                grid.selection.clear();
                                                grid.selection.setSelected(item, true);

                                                dynamicPaneUrl = item.dynamic_pane_url;

                                                request(dynamicPaneUrl).then(

                                                  function(json){
                                                    var jsondata = JSON.parse(json);
                                                    var args = { title     : jsondata.title, 
                                                                domId     : jsondata.id,
                                                                url       : jsondata.url,
                                                                parentTab : registry.byId( jsondata.parentTab )
                                                            };
//                                                   console.log( args );
                                                    createDynamicHTMLPane( args );

                                                  },
                                                  function(err){
                                                    publishError(err.response.text);
                                                  }
                                                );
//                                                 return false;

                }

                grid.startup();                
                console.log(grid);
                return grid;
        },

        setupReadOnlyGrid: function (gridUrl, gridDomNode, gridStr, activateRowClick, gridName, storeToUse) {

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
                        structure: gridStr,
                        noDataMessage: "<span class='dojoxGridNoData'>No Matching Data</span>"
                    },
                    gridDomNode
                );

                grid.activateRowClick = activateRowClick;

                grid.title = gridName ? gridName.toString():"Patient";

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

//                     if (grid.activateRowClick) {
//                       auEventController.onPatientGridSelect(item);
//                     }
//                     else{ 
                      return false; 
//                     }

                }

                grid.onRowDblClick = function(e){ 
                                    return false;
//                                         onGridRowDblClick({event: e, 
//                                                            grid: grid, 
//                                                            title: grid.title,
//                                                            gridId : gridDomNode
//                                                           });
                }

                grid.startup();                
                console.log(grid);
                return grid;
            }

            
      }

});
