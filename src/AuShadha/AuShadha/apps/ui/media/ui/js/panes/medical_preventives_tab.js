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
                          {id: "patientMedicalPreventivesTab"},
                          "patientPreventiveTabs",
                          "last"
      );

          domConstruct.create('div',
                              {id: "medical_preventives_list"},
                              "patientMedicalPreventivesTab",
                              "first"
          );
    }

    function makeDijits(){
      var preventiveHealthTabs  =  registry.byId('patientPreventiveTabs');
      var patientMedicalPreventivesTab = new ContentPane({
                                                        id:"patientMedicalPreventivesTab",
                                                        title:"Medical Preventives",
                                                         closable:true,
                                                         doLayout:true
                                                        },
                                                        "patientMedicalPreventivesTab"
                                                        );
      preventiveHealthTabs.addChild(patientMedicalPreventivesTab);

          var patientMedicalPreventivesList = new ContentPane({id:"medical_preventives_list",
                                                      },
                                                      "medical_preventives_list"
                                                      );
          patientMedicalPreventivesTab.addChild(patientMedicalPreventivesList);
          registry.byId('medical_preventives_list').set('href', urlObj.medicalPreventivesUrl);
          registry.byId('patientContextTabs').
            selectChild( registry.byId('patientPreventiveHealthTab') )
          registry.byId('patientPreventiveTabs').
            selectChild( registry.byId('patientMedicalPreventivesTab') )

    }

    makeDoms();
    makeDijits();

});

}