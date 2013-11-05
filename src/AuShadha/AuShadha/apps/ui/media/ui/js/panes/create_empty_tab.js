define([
          "dojo/dom",
          "dojo/dom-style",
          "dojo/query",
          "dojo/dom-construct",
          'dojo/dom-attr',

          "dijit/registry",
          "dijit/form/Button",
          "dojox/layout/ContentPane",
          "dijit/layout/TabContainer",
          "dijit/layout/BorderContainer"
  ],
  function(dom,
           domStyle,
           query,
           domConstruct,
           domAttr,
           registry,
           Button,
           ContentPane,
           TabContainer,
           BorderContainer){

    var tab = {
          makeDoms : function(){
                              domConstruct.create('div',
                                                  {id:tab.module_name+"_tab"},
                                                  tab.parent,
                                                  "after"
                              );
                  },

          makeDijits : function (){

                        var emptyTab = new ContentPane({ title : tab.module_title,
                                                        closable  : true,
                                                        iconClass : "contactIcon"
                                                      },
                                                      tab.module_name+"_tab"
                        );
                        registry.byId(tab.parent).addChild(emptyTab);

//                         emptyTab.startup();

//                         registry.byId(tab.parent).selectChild(emptyTab);

                        tab.pane = emptyTab;
                        tab.domNode = emptyTab.domNode;
          },

          addBc: function(layout,sections){
                      var Bc = BorderContainer({style:"height:100%; width:100%;"},
                                               domConstruct.create('div',
                                                                   {id: domAttr.get(tab.pane.domNode,'id')+"_main_BC"},
                                                                   tab.pane.domNode,
                                                                   0)
                      );
                      console.log("Created BorderContainer " );

                      tab.pane.Bc = Bc;

                      if(layout){
                        if (layout == 'vertical'){
                          tab.layoutVertical(sections);
                        }else if (layout == 'horizontal'){
                          tab.layoutHorizontal(sections);
                        }
                      }

                      Bc.startup();
                      tab.pane.addChild(Bc);

          },

          layoutVertical: function(sections){
                      var pDom = tab.pane.Bc.domNode;
                      var domId = domAttr.get(tab.pane.Bc.domNode, 'id') + "_cp";

                      if (sections && sections > 1){
                        var cp_top = ContentPane({region:'center',
                                                splitter:true
                                               },
                                               domConstruct.create('div',
                                                                   {id:domId+"_top"},
                                                                   pDom,
                                                                   0
                                                                  )
                        );
                        tab.pane.Bc.topCp = cp_top;

                        var cp_bottom = ContentPane({region:'bottom',
                                                    splitter:true,
                                                    style:"height:15em;"
                                                    },
                                                    domConstruct.create('div',
                                                                        {id: domId+"_bottom"},
                                                                        pDom,
                                                                        1
                                                                      )
                        );
                        tab.pane.Bc.bottomCp = cp_bottom;

                        cp_top.startup();
                        cp_bottom.startup();

                        tab.pane.Bc.addChild(cp_top);
                        tab.pane.Bc.addChild(cp_bottom);
                      }else if(sections && sections ==1){
                        var cp_top = ContentPane({region:'center',
                                                splitter:true
                                               },
                                               domConstruct.create('div',
                                                                   {id:domId+"_top"},
                                                                   pDom,
                                                                   0
                                                                  )
                        );
                        tab.pane.Bc.topCp = cp_top;
                        cp_top.startup();
                        tab.pane.Bc.addChild(cp_top);                        
                      }
          },

          layoutHorizontal: function(sections){
                      var pDom = tab.pane.Bc.domNode;
                      var domId = domAttr.get(tab.pane.Bc.domNode, 'id') + "_cp";

                      var cp_left = ContentPane({region:'leading',splitter:true,style:"width:25em;"},
                                                  domConstruct.create('div',
                                                                      {id:domId+"_left"},
                                                                      pDom, 
                                                                      0
                                                                     )
                      );
                      tab.pane.Bc.leftCp = cp_left;

                      var cp_center = ContentPane({region:'center',splitter:true},
                          domConstruct.create('div',
                                              {id: domId+"_center"}, 
                                              pDom,
                                              1
                                             )
                      );
                      tab.pane.Bc.centerCp = cp_center;

                      cp_left.startup();
                      cp_center.startup();

                      tab.pane.Bc.addChild(cp_left);
                      tab.pane.Bc.addChild(cp_center);
          }

    }
    return{
      constructor: function(obj){

                      console.log(obj);

                      if (registry.byId(obj.module_name+'_tab')){
                        var child = registry.byId(obj.module_name+'_tab')
                        var immParent = registry.byId(obj.module_name+'_tab').getParent();
                        immParent.removeChild(child);
                        child.destroyRecursive();
                      }

                      if (!registry.byId(obj.module_name+'_tab')){                        
                           tab.parent = obj.parent;
                           tab.module_name = obj.module_name;
                           tab.module_title = obj.module_title;
                            
                           tab.makeDoms();
                           tab.makeDijits();

                      }else{
                        registry.byId(obj.parent).
                                  selectChild(
                                         registry.byId(obj.module_name+'_tab')
                                  );
                        tab.pane = registry.byId(obj.module_name+'_tab');
                        tab.domNode = tab.pane.domNode;
                      }

                      console.log(tab.addBc);
                      return tab;
      }
    }

});