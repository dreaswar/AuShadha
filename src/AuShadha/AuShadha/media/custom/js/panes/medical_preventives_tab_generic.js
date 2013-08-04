define([
      "dojo/dom",
      "dojo/dom-style",
      "dojo/query",
      "dojo/dom-construct",

      "dijit/registry",
      "dijit/form/Button",
      "dojox/layout/ContentPane",
      "dijit/layout/TabContainer",
      "dijit/layout/BorderContainer",

      'aushadha/grid/grid_structures',
      'aushadha/grid/grid_setup'
    ], 
    function(dom, 
             domStyle,
             query,
             domConstruct, 
             registry, 
             Button,
             ContentPane, 
             TabContainer, 
             BorderContainer,

             GRID_STRUCTURES,
             auGridSetup
            ){

        var __mainWidgetLabel__ = '';
        var __tabTitle          = '';
        var _widgetState        = dom.byId(nodeIds.widget);

        var nodeIds={
          parent          : '',
          widget          : nodeIds.parent+ __mainWidgetLabel__ + 'Tab',
          widgetContainer : nodeIds.widget+ '_Container',
          widgetList      : nodeIds.widget+ '_List',
        }

        function makeDoms(){
            domConstruct.create('div',
                                {id   :nodeIds.widget, 
                                 style:"height:auto;overflow:auto;position:relative;float:left;"
                                },
                                nodeIds.parent,
                                "after"
            );

            domConstruct.create("div",
                                {"id":widgetContainer},
                                nodeIds.widget,
                                "first"
            );
              domConstruct.create("div",
                                  {"id":nodeIds.widgetList},
                                  nodeIds.widgetContainer,
                                  "first"
                  );
        }

        function makeDijits(){
            
            /*Create the widget and add it as a Tab to the Parent */
            var widgetTab = new ContentPane({ title     : __tabTitle,
                                              closable  : true,
                                              iconClass : "contactIcon"
                                             },
                                            nodeIds.widget
            );
            registry.byId(nodeIds.parent).addChild(widgetTab);

            /*Starup the Widget */
            widgetTab.startup();

            /* Select the newly added Tab and Call resize on the parent BorderContainer */
            registry.byId(nodeIds.parent).selectChild(nodeIds.widget);
            registry.byId("patientTabsBorderContainer").resize();

        }

        function makeGrid(grid){
          /*Create Appropriate Grids*/ // 
          return auGridSetup.gridSetupFn(grid);
        }

        function makeButton( obj /*{label:String,
                                    title:String,
                                    onClickUrl:String}
                                 */){
            var button =  new Button({label   : obj.label,
                                      title   : obj.title,
                                      iconClass   : "dijitIconNewTask",
                                      onClick : function(){
                                                require(["dojo/_base/xhr", "dojo/_base/array"],
                                                function(xhr, array){
                                                    xhr.get({
                                                            url: obj.onClickUrl,
                                                            load: function(html){
                                                                          var myDialog = dijit.byId("editPatientDialog");
                                                                          myDialog.set('content', html);
                                                                          myDialog.set('title', "Add "+obj.title);
                                                                          myDialog.show();
                                                                  }
                                                    });
                                                });
                                              }
                                      },
                                      domConstruct.create('button',
                                                          {type : "button",
                                                          id   : "add" + obj.title + "Button"
                                                          },
                                                          nodeIds.widgetList,
                                                          "before"
                                      )
                                    );
         return button;
        }

    return {
     constructor: function(obj /* {widget:{label : String,title : String, parent: String}, 
                                   grid  : {storeUrl: String, gridSetupFn: Fn },
                                   button: {label:'',title:'',onClickUrl:''} }
                               */){
                        __mainWidgetLabel__ = obj.widget.label;
                        __tabTitle          = obj.widget.title;               
                        nodeIds.parent      = obj.widget.parent;
                        storeUrl            = obj.grid.storeUrl;
                        gridSetupFn         = obj.grid.gridSetupFn;

                        makeDoms(obj.widget);
                        makeDijits();
                        makeGrid(obj.grid);
                        makeButton(obj.button);
                  }
    }

});