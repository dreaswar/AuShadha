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
                                                    {id: tab.module_name+"_add_or_edit_form"},
                                                    domAttr.get(tab.parentPane.domNode,'id'),
                                                    "first"
                                );
                                domStyle.set(tab.module_name+'_add_or_edit_form',{height:"30em"});
                               console.log("Made the FormContainer DOMS");
                  },

          makeDijits : function (){

                        var AddOrEditForm = new ContentPane({ id:tab.module_name+"_add_or_edit_form",
                                                              href: tab.urlToCall
                                                        },
                                                        tab.module_name+"_add_or_edit_form"
                                                        );
                        console.log("Made the FormContainer Dijits");

                         tab.parentPane.addChild(AddOrEditForm);
                        console.log("Added the FormContainer Dijits");
                        tab.pane = AddOrEditForm;
                        console.log("Set the Tab Attribute...");
                      }
    }
    return{
      constructor: function(obj){

                      console.log("Received the request to make a FormContainer");
                      var domId = obj.module_name+"_add_or_edit_form";
                      console.log("checking for tab with ID: "+ domId);

                      if (!registry.byId(domId) ){                        
                          console.log("Form Container Does not exist.. making a new one..");
                          tab.urlToCall = obj.url;
                          tab.parentPane = obj.parentPane;
                          tab.module_name = obj.module_name;
                          tab.module_title = obj.module_title;

                          tab.makeDoms();
                          tab.makeDijits();
                          console.log(tab.pane);
                      }else{
                        console.log("Form Container Exists ! ");
                        tab.parentPane = obj.parentPane;
                        tab.urlToCall = obj.url
                        tab.module_name = obj.module_name;
                        tab.module_title = obj.module_title;
                        tab.pane = registry.byId( domId );
                        var p = obj.parentPane.getParent();
                        p.selectChild( obj.parentPane );
                      }
                     return tab.pane;
      }
    }

});