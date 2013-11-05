define(['dijit/registry',
       'dojo/dom',
       'dojo/dom-construct',
       'dojo/dom-class',
       'dojo/dom-attr',
       'dijit/layout/BorderContainer',
       'dijit/layout/TabContainer',
       'dojox/layout/ContentPane'
       ],

function(registry,
         dom,
         domConstruct,
         domClass,
         domAttr,
         BorderContainer,
         TabContainer,
         ContentPane
        ){

  function createSubModulePane(d,p,title,domId){

        var centerTopTabPane = registry.byId('centerTopTabPane');

        if (!d) {

              var d = domConstruct.create('div', 
                                          {id: domId+"_main"},
                                          centerTopTabPane.domNode,
                                          'last');

              var bc = domConstruct.create('div', 
                                          {id: domId+"_bc"},
                                          d,
                                          0);

              var top = domConstruct.create('div', 
                                          {id: domId+"_top"},
                                          bc,
                                          0);

              var center = domConstruct.create('div', 
                                          {id: domId+"_center"},
                                          bc,
                                          1);

              var form_container = domConstruct.create('div', 
                            {id: domId+"_center_form_container"},
                            center,
                            0);

              var left = domConstruct.create('div', 
                            {id: domId+"_leading"},
                            bc,
                            2);

              var grid_container = domConstruct.create('div', 
                            {id: domId+"_leading_grid_container"},
                            left,
                            0);
        }

        if (!p){

            console.log("Creating widget with ID: " + domId+"_main");
            var p = new ContentPane({title: title, 
                                    id: domId+"_main"
                                    },
                                    domId+"_main");

            console.log("Creating widget with ID: " + domId+"_bc");
            var b_dijit = new BorderContainer({id: domId+"_bc"},
                                              domId+"_bc"
                                             );

            console.log("Creating widget with ID: " + domId+"_top");
            var top_dijit = new ContentPane({region:'top',
                                             class : "topContentPane",
                                             id: domId+"_top"
                                            },
                                            domId+"_top");

            console.log("Creating widget with ID: " + domId+"_center");
            var center_dijit = new ContentPane({region: 'center',
                                                id: domId+"_center"
                                              }, 
                                              domId+"_center");

            console.log("Creating widget with ID: " + domId+"_leading");
            var left_dijit = new ContentPane({region: 'leading',
                                              splitter: true,
                                              style:'width: 48em;',
                                              id: domId+"_leading"
                                             },
                                             domId+"_leading");

            b_dijit.addChild(top_dijit);
            b_dijit.addChild(center_dijit);
            b_dijit.addChild(left_dijit);

            p.addChild(b_dijit);
            centerTopTabPane.addChild(p);              
        }

        centerTopTabPane.selectChild(p);

  }

    return createSubModulePane;

});