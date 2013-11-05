define([
          "dojo/dom",
          "dojo/dom-style",
          "dojo/query",
          "dojo/dom-construct",

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
                              domStyle.set(tab.module_name+'_tab',{"height":"auto","overflow":"auto"});
                                domConstruct.create('div',
                                                    {id: tab.module_name+"_add_or_edit_form"},
                                                    tab.module_name+"_tab",
                                                    "first"
                                );

                                domStyle.set(tab.module_name+'_add_or_edit_form',{height:"30em"});
                  },

          makeDijits : function (){

                        var formTab = new ContentPane({ title : tab.module_title,
                                                    closable  : true,
                                                    iconClass : "contactIcon"
                                                  },
                                                  tab.module_name+"_tab"
                        );
                        registry.byId(tab.parent).addChild(formTab);

                        var AddOrEditForm = new ContentPane({ id:tab.module_name+"_add_or_edit_form",
                                                              href: tab.urlToCall
                                                        },
                                                        tab.module_name+"_add_or_edit_form"
                                                        );
                        formTab.addChild(AddOrEditForm);

                        formTab.startup();

                        registry.byId(tab.parent).selectChild(formTab);
                        
                        tab.pane = formTab;
                      }
    }
    return{
      constructor: function(obj){
                      console.log(obj);
                      if (!registry.byId(obj.module_name+'_tab')){                        
                          tab.urlToCall = obj.url;
                          tab.parent = obj.parent;
                          tab.module_name = obj.module_name;
                          tab.module_title = obj.module_title;

                          tab.makeDoms();
                          tab.makeDijits();
                          console.log(tab.pane);
                          return tab.pane;
                      }else{
                        registry.byId(obj.parent).
                                  selectChild(
                                         registry.byId(obj.module_name+'_tab')
                                  );                        
                      }
      }
    }

});