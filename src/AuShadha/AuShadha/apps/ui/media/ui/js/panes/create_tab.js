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
             auGridSetup
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

            createDoms: function (){
              domConstruct.create('div',
                                      {id: domVars.id},
                                      domVars.parent,
                                      "last"
                  );

              domConstruct.create('div',
                                  {id: gridVars.id},
                                  domVars.id,
                                  0
              );
              console.log(domVars);
              console.log(gridVars);
              console.log(btnVars);
          },

          createDijits: function (){

              if(registry.byId(domVars.id)){
                registry.byId(domVars.id).destroyRecursive(true);
              }
                var tab = new ContentPane({id      : domVars.id,
                                          title    : domVars.title,
                                          closable : true
                                          },
                                          domVars.id);
                registry.byId(domVars.parent).addChild(tab);

          },

          createButtons: function (){

                    var addButton =  new Button({
                                                label       : btnVars.label,
                                                title       : domVars.title,
                                                iconClass   : "dijitIconNewTask",
                                                onClick: function(){
                                                      require(
                                                        ["dojo/_base/xhr", "dojo/_base/array"],
                                                        function(xhr, array){
                                                          xhr.get({
                                                            url: btnVars.url,
                                                            load: function(html){
                                                                      var myDialog = registry.byId("editPatientDialog");
                                                                      window.CHOSEN_GRID = gridVars.id;
                                                                      myDialog.set('content', html);
                                                                      myDialog.set('title', domVars.title);
                                                                      myDialog.show();
                                                                  }
                                                        });
                                                      })
                                                }
                              },
                              domConstruct.create('button',
                                                  {type : "button",
                                                  },
                                                  gridVars.id,
                                                  "before"
                              )
                );

          },

          fillData: function (){

              var gridTitle = btnVars.title.split(' ')[1].toString();
              var storeToUse = gridTitle.toUpperCase() + "_GRID_STORE";

              auGridSetup.setupGrid(gridVars.url,
                                    gridVars.id,
                                    gridVars.str,
                                    false,
                                    gridTitle,
                                    storeToUse
                                    );

              registry.byId(domVars.parent).selectChild(domVars.id);

          }
        
      }

      return {
        constructor: function(obj){
                        console.log("Received Obj to load a tab: ");
                        console.log(obj);

                        domVars = obj.dom;
                        gridVars = obj.grid;
                        btnVars = obj.button;

                        tab.parent = dom.byId(domVars.parent);
                        tab.widgets_allowed=[];

                        tab.createDoms();
                        tab.createDijits();
                        tab.createButtons();
                        tab.fillData();

                        }
      }


});