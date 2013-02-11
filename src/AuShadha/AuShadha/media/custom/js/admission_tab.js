function setUpAdmissionTab(){
  require(
  ["dijit/registry",
   "dojo/parser",
   "dijit/layout/BorderContainer",
   "dijit/layout/TabContainer",
   "dojox/layout/ContentPane",
   //"dojox/layout/ExpandoPane",
   "dijit/Editor",
   "dijit/form/Button",
   "dojo/dom",
   "dojo/dom-construct",
   "dojo/dom-style",
   "dojo/ready",
   "dojo/_base/array",
   "dojo/request/xhr"
  ],
  function(registry,parser, BorderContainer,
           TabContainer, ContentPane, /*ExpandoPane,*/ Editor,Button,
           dom, domConstruct, domStyle, ready,array,xhr
  ){

    var main_tab_container = registry.byId("centerTopTabPane");
    //var admission_tab  = registry.byId('admissionHomeContentPane');

    function createOrSelectTab(){
      console.log("Starting to create / select admission tab as necessary...");
      if( registry.byId('admissionHomeContentPane') == false ){
        console.log("Starting to create the Admission Tab DOMS.");
        domConstruct.create('div',
                            {id:'admissionHomeContentPane'},
                            registry.byId('centerTopTabPane').domNode,
                            'last');

        var admissionPane = new ContentPane({id       : "admissionHomeContentPane",
                                         closable : true,
                                         disabled : false,
                                         selected : true,
                                         closable: false
                                        },
                                        'admissionHomeContentPane'
                                       );
        main_tab_container.addChild(admissionPane);

      }

      else{
        console.log("Admission Tab already present.. so not creating. Selecting the same..");
        var admission_tab  = registry.byId('admissionHomeContentPane');
        admission_tab.set('disabled',false);
        admission_tab.set('closable',false);
        main_tab_container.selectChild(admission_tab);
      }

      var topBarHTML = dom.byId('selected_patient_info').innerHTML;
      dom.byId('admissionPaneTopbar').innerHTML = topBarHTML;

//    fillTabWithDomAndDijits();
    }

    function fillTabWithDomAndDijits(){
      // Fill the Tab with appropriate Dom and Dijits
      console.log("Starting to fill contents into admission tab....");

      domConstruct.create('div',{id: "admissionPaneContentBorderContainer",style: "height: 100%; width: 100%"},'admissionHomeContentPane','first');
      domConstruct.create('div',{id: "admissionPaneLSidebar", style: "height: 100%; width: 20em"},'admissionPaneContentBorderContainer',0);
      domConstruct.create('div',{id: "admissionPaneContentArea" /*, style: "height: 100%; width: 100em"*/},'admissionPaneContentBorderContainer',1);

      console.log("created the DOMS");

      var admissionPaneContentBorderContainer = new BorderContainer({id:"admissionPaneContentBorderContainer"});
      var admissionLSidebar    = new ContentPane({id       : "admissionLSidebar",region: 'leading', splitter:true},
                                        'admissionLSidebar'
                                       );
      var admissionContentArea = new ContentPane({id       : "admissionContentArea", region: 'center'},
                                        'admissionContentArea'
                                       );
      console.log("created the Dijits");

      var main_admission_tab = registry.byId('admissionHomeContentPane');

      main_admission_tab.addChild(admissionPaneContentBorderContainer);
        admissionPaneContentBorderContainer.addChild(admissionLSidebar);
        admissionPaneContentBorderContainer.addChild(admissionContentArea);
      console.log("added the Dijits");

       admissionPaneContentBorderContainer.placeAt(dom.byId('admissionPaneContentBorderContainer'));
       admissionPaneContentBorderContainer.startup();

      console.log("Dijits Started...");
    }

    createOrSelectTab();

//  function fillTabWithDomAndDijits(){
//    // Fill the Tab with appropriate Dom and Dijits
//  }

  });
}