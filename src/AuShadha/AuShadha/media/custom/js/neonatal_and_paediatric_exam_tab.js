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
                          {id: "patientNeonatalAndPaediatricExamTab"},
                          "patientPreventiveTabs",
                          "last"
      );

          domConstruct.create('div',
                              {id: "neonatal_and_paediatric_exam"},
                              "patientNeonatalAndPaediatricExamTab",
                              "first"
          );
    }

    function makeDijits(){
      var preventiveHealthTabs  =  registry.byId('patientPreventiveTabs');
      var patientNeonatalAndPaediatricExamTab = new ContentPane({
                                                        id:"patientNeonatalAndPaediatricExamTab",
                                                        title:"Neonatal & Paediatric Exam",
                                                         closable:true,
                                                         doLayout:true
                                                        },
                                                        "patientNeonatalAndPaediatricExamTab"
                                                        );
      preventiveHealthTabs.addChild(patientNeonatalAndPaediatricExamTab);

          var patientNeonatalAndPaediatricExam = new ContentPane({id:"neonatal_and_paediatric_exam",
                                                      },
                                                      "neonatal_and_paediatric_exam"
                                                      );
          patientNeonatalAndPaediatricExamTab.addChild(patientNeonatalAndPaediatricExam);
          registry.byId('neonatal_and_paediatric_exam').set('href', urlObj.neonatalAndPaediatricExamUrl);
          registry.byId('patientContextTabs').
            selectChild( registry.byId('patientPreventiveHealthTab') )
          registry.byId('patientPreventiveTabs').
            selectChild( registry.byId('patientNeonatalAndPaediatricExamTab') )

    }

    makeDoms();
    makeDijits();

});

}