function(urlObj /* URL Object */){
  require([
          "dojo/dom",
          "dojo/dom-style",
          "dojo/dom-construct",

          "dijit/registry",
          "dijit/form/Button",
          "dojox/layout/ContentPane",
          "dijit/layout/TabContainer",
          "dijit/layout/BorderContainer",
  ],
  function(dom,
           domStyle,
           domConstruct,
           registry,
           Button,
           ContentPane,
           TabContainer,
           BorderContainer){

    function makeDoms(){
      domConstruct.create('div',
                          {id: "patientSurgicalPreventivesTab"},
                          "patientPreventiveTabs",
                          "last"
      );

          domConstruct.create('div',
                              {id: "surgical_preventives_list"},
                              "patientSurgicalPreventivesTab",
                              "first"
          );
    }

    function makeDijits(){
      var preventiveHealthTabs  =  registry.byId('patientPreventiveTabs');
      var patientSurgicalPreventivesTab = new ContentPane({
                                                        id:"patientSurgicalPreventivesTab",
                                                        title:"Surgical Preventives",
                                                         closable:true,
                                                         doLayout:true
                                                        },
                                                        "patientSurgicalPreventivesTab"
                                                        );
      preventiveHealthTabs.addChild(patientSurgicalPreventivesTab);

          var patientSurgicalPreventivesList = new ContentPane({id:"surgical_preventives_list",
                                                      },
                                                      "surgical_preventives_list"
                                                      );
          patientSurgicalPreventivesTab.addChild(patientSurgicalPreventivesList);
          registry.byId('surgical_preventives_list').set('href', urlObj.surgicalPreventivesUrl);
          registry.byId('patientContextTabs').
            selectChild( registry.byId('patientPreventiveHealthTab') )
          registry.byId('patientPreventiveTabs').
            selectChild( registry.byId('patientSurgicalPreventivesTab') )

    }

    makeDoms();
    makeDijits();

});

}