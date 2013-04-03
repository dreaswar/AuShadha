function (tabId, tabTitle, formId, urlToCall){
  require([
          "dojo/dom",
          "dojo/dom-style",
          "dojo/query",
          "dojo/dom-construct",

          "dijit/registry",
          "dijit/form/Button",
          "dojox/layout/ContentPane",
          "dijit/layout/TabContainer",
          "dijit/layout/BorderContainer",
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

    function makeDoms(){
      console.log("Making DOMS ");
      domConstruct.create('div',
                          {id:tabId},
                          'patientSummaryTab',
                          "after"
      );
      domStyle.set(tabId,{"height":"auto","overflow":"auto"});

      if(formId){
        domConstruct.create('div',
                            {id: formId },
                            tabId,
                            "first"
        );
        domStyle.set(formId,{height:"30em"});
      }

    }

    function makeDijits(){
      console.log("Making Dijits ..");
      var Tab = new ContentPane({ title     : tabTitle,
                                  closable  : true,
                                  iconClass : "contactIcon"
                                },
                                tabId
      );
      registry.byId('patientContextTabs').addChild(Tab);

      if(formId){
        var AddOrEditForm = new ContentPane({
                                            id   : formId,
                                            href : urlToCall
                                        },
                                        formId
                                        );
        Tab.addChild(AddOrEditForm);
      }

      Tab.startup();
      registry.byId("patientContextTabs").selectChild(tabId);
      registry.byId("patientTabsBorderContainer").resize();

    }

  makeDoms();
  makeDijits();

  });


}