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

  function createMainModulePane(d,p,title,domId, closable){

        var centerTopTabPane = registry.byId('centerTopTabPane');

        if (!d) {

              console.log(d);
              var d = domConstruct.create('div', 
                                          {id: domId+"_main"},
                                          centerTopTabPane.domNode,
                                          'last');

              var bc = domConstruct.create('div', 
                                          {id: domId+"_bc"},
                                          d,
                                          0);

              console.log("Created Pane: ", bc);
              var top = domConstruct.create('div', 
                                          {id: domId+"_top"},
                                          bc,
                                          0);

              var center = domConstruct.create('div', 
                                          {id: domId+"_center"},
                                          bc,
                                          1);

              var c_tc = domConstruct.create('div', 
                                        {id: domId+"_center_tc"},
                                        center,
                                        0);

              var summary_t = domConstruct.create('div', 
                                                    {id: domId+"_center_summary_tab"},
                                                    c_tc,
                                                    0);

              var summary_div = domConstruct.create('div', 
                                  {id: domId+"_summary_div"},
                                  summary_t,
                                  0);

              var left = domConstruct.create('div', 
                            {id: domId+"_leading"},
                            bc,
                            2);

              var tree = domConstruct.create('div', 
                              {id: domId+"_leading_tree"},
                              left,
                              0);
            }

            if (!p){

              if (! window.CHOSEN_PATIENT ) {
                var disabled = true;
              }
              else{
                var disabled = false;
              }

              if (! closable){
                closable = false;
              }
              else{
                closable = true
              }
              
              var p = new ContentPane({title: title,
                                       id: domId+"_main",
                                       disabled: disabled,
                                       closable : closable,
                                       class : "mainTabContainer",
                                       scriptHasHooks: true,
                                       executeScripts: true
                                      },
                                      domId+"_main");

              var b_dijit = new BorderContainer({id: domId+"_bc"},domId+"_bc");

              var top_dijit = new ContentPane({region:'top',
                                               class : "topContentPane",
                                               id: domId+"_top",
                                               scriptHasHooks: true,
                                               executeScripts: true
              },
                                              domId+"_top");

              var center_dijit = new ContentPane({region: 'center',
                                                  id: domId+"_center",
                                                  scriptHasHooks: true,
                                                  executeScripts: true
              },
                                                 domId+"_center");

              var left_dijit = new ContentPane({region: 'leading',
                                                splitter: true,
                                                style:'width: 18em;',
                                                id: domId+"_leading",
                                                scriptHasHooks: true,
                                                executeScripts: true
              },
                                               domId+"_leading");

              b_dijit.addChild(top_dijit);
              b_dijit.addChild(center_dijit);
              b_dijit.addChild(left_dijit);

              var c_tc_dijit = new TabContainer({tabStrip: true, 
                                                 tabPosition:'top',
                                                 id: domId+"_center_tc",
                                                class: "subTabContainer"
                                                },
                                                domId+"_center_tc");

              center_dijit.addChild(c_tc_dijit);

              var summary_t_dijit = new ContentPane({title: "Summary", 
                                                    id: domId+"_center_summary_tab",
                                                    scriptHasHooks: true,
                                                    executeScripts: true
                                                    },
                                                    domId+"_center_summary_tab");

              c_tc_dijit.addChild(summary_t_dijit);

              p.addChild(b_dijit);
              centerTopTabPane.addChild(p);
              
              return c_tc? c_tc:c_tc_dijit.domNode
            }

            centerTopTabPane.selectChild(p);
      }

    return createMainModulePane;

});