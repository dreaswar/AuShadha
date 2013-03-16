function (urlToCall){
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
      console.log("Making DOMS for Social History Form..");
      domConstruct.create('div',
                          {id:"socialHistoryTab"},
                          'patientSummaryTab',
                          "after"
      );
      domStyle.set('socialHistoryTab',{"height":"auto","overflow":"auto"});
        domConstruct.create('div',
                            {id: "social_history_add_or_edit_form"},
                            "socialHistoryTab",
                            "first"
        );

        domStyle.set('social_history_add_or_edit_form',{height:"30em"});


    }

    function makeDijits(){
      console.log("Making Dijits for Social History Form..");
      var socialHistoryTab = new ContentPane({ title     : "Social History",
                                              closable  : true,
                                              iconClass : "contactIcon"
                                            },
                                            "socialHistoryTab"
      );
      registry.byId('patientContextTabs').addChild(socialHistoryTab);

      var socialHistoryAddOrEditForm = new ContentPane({
                                              id:"social_history_add_or_edit_form",
                                              href: urlToCall
                                      },
                                      "social_history_add_or_edit_form"
                                      );
      socialHistoryTab.addChild(socialHistoryAddOrEditForm);

      socialHistoryTab.startup();

      registry.byId("patientContextTabs").selectChild("socialHistoryTab");
      registry.byId("patientTabsBorderContainer").resize();

    }

  makeDoms();
  makeDijits();

  });


}