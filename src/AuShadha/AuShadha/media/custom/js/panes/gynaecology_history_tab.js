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
                          {id: "patientGynaecologyPreventivesTab"},
                          "patientPreventiveTabs",
                          "last"
      );

          domConstruct.create('div',
                              {id: "gynaecology_history_detail"},
                              "patientGynaecologyPreventivesTab",
                              "first"
          );
    }

    function makeDijits(){
      var preventiveHealthTabs  =  registry.byId('patientPreventiveTabs');
      var patientGynaecologyPreventivesTab = new ContentPane({id:"patientGynaecologyPreventivesTab",
                                                        title:"Gynaecology History",
                                                         closable:true,
                                                         doLayout:true
                                                        },
                                                        "patientGynaecologyPreventivesTab"
                                                        );
      preventiveHealthTabs.addChild(patientGynaecologyPreventivesTab);

          var patientGynaecologyHistoryDetail = new ContentPane({id:"gynaecology_history_detail",
                                                      },
                                                      "gynaecology_history_detail"
                                                      );
          patientGynaecologyPreventivesTab.addChild(patientGynaecologyHistoryDetail);
          registry.byId('gynaecology_history_detail').set('href', urlObj.gynaecologyHistoryUrl);
          registry.byId('patientContextTabs').
            selectChild( registry.byId('patientPreventiveHealthTab') )
          registry.byId('patientPreventiveTabs').
            selectChild( registry.byId('patientGynaecologyPreventivesTab') )

    }

    makeDoms();
    makeDijits();

});

}