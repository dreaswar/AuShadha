define([
        "dojo/dom",
        'dojo/dom-class',
        'dojo/dom-style',
        'dojo/dom-construct',
        'dojo/on',

        'dijit/registry',
        'dijit/layout/BorderContainer',
        'dojox/layout/ContentPane',
        'dijit/layout/TabContainer',
        'dijit/form/Button',
        "dijit/Dialog",
        "dojo/request",
        "dojo/json",
        "dojo/_base/lang",

       'aushadha/grid/grid_structures',
       'aushadha/grid/generic_grid_setup',
       'aushadha/panes/create_add_button',

        "dojo/domReady!",
    ],
    function(dom,
             domClass,
             domStyle,
             domConstruct,
             on,
             registry,
             BorderContainer,
             ContentPane,
             TabContainer,
             Button,
             Dialog,
             request,
             JSON,
             lang,

             GRID_STRUCTURES,
             auGridSetup,
             createGridButton
    ){

          var domVars={};
          var gridVars={};
          var btnVars = {};

          var tab = {
            
            parent:'',

            module_type:'',

            widgets_allowed:'',

            widgets:[],

            layout:[],
       
            button: [],

            createDoms: function (){
                domConstruct.create('div',
                                    {id: domVars.id},
                                    domVars.parent,
                                    "last"
                );

                console.log("Created Tab DOM after " + domVars.parent + " DOM id");
                domConstruct.create('div',
                                    {id: gridVars.id},
                                    domVars.id,
                                    0
                );
                console.log("Created Grid DOM after " + domVars.id + " DOM id with ID of " + gridVars.id );

//                 console.log(domVars);
//                 console.log(gridVars);
//                 console.log(btnVars);
            },

            createDijits: function (){

//                 if(registry.byId(domVars.id)){
//                   registry.byId(domVars.id).destroyRecursive(true);
//                 }
                console.log("Creating all the ContentPane Dijits in preparation to creating a Grid");
                var gridTab = new ContentPane({id      : domVars.id,
                                              title    : btnVars.title.split(' ')[1].toString(),
                                              closable : false
                                              },
                                              domVars.id);
                tab.pane = gridTab;
                registry.byId(domVars.parent).addChild(gridTab);
                console.log("Added all the ContentPane Dijits in preparation to creating a Grid");

            },

            createButtons: function (){
                          console.log("Creating Button to place above Grid");                            
                          var button = createGridButton.constructor({gridId: gridVars.id, 
                                                                    label: btnVars.label, 
                                                                    title: btnVars.title,
                                                                    url: btnVars.url
                                                                  });
                          tab.button.push(button);
                          console.log("Added the AddButton above the Grid");                            
            },

            fillData: function (){
                console.log("About to create the Grid");
                var gridTitle = btnVars.title.split(' ')[1].toString();
                var storeToUse = gridTitle.toUpperCase() + "_GRID_STORE";
                console.log("Using Store: ");
                console.log(storeToUse);
                console.log("About to creat GRID with these arguments ");
                var args = {url: gridVars.url,
                            id:  gridVars.id,
                            str: gridVars.str,
                            activateRowClick: false,
                            gridTitle: gridTitle,
                            storeToUse: storeToUse
                }
                console.log(args);
                var grid = auGridSetup.setupGrid(gridVars.url,
                                                 gridVars.id,
                                                 gridVars.str,
                                                 false,
                                                 gridTitle,
                                                 storeToUse
                                                );
                tab.grid = grid;
                console.log("Created the Grid with ID: " + gridVars.id);
  //               registry.byId(domVars.parent).selectChild(domVars.id);
            }

      }

      return {
        constructor: function(obj){
                        console.log("Received Obj to load a tab: ");
                        console.log(obj);

                        domVars = obj.dom;    /* has id, title and parent attributes   */
                        gridVars = obj.grid;  /* has url, structure, and id attributes */
                        btnVars = obj.button; /* has label, add url attributes         */

                        tab.parent = dom.byId(domVars.parent);

                        tab.createDoms();
                        tab.createButtons();
                        tab.createDijits();
                        tab.fillData();
                        return tab.pane;
                    }
      }


});