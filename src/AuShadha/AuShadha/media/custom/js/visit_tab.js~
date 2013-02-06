function setUpVisitTab(){
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
    //var visit_tab  = registry.byId('visitHomeContentPane');

    function createOrSelectTab(){
      console.log("Starting to create / select visit tab as necessary...");
      if( registry.byId('visitHomeContentPane') == false ){
        console.log("Starting to create the Visit Tab DOMS.");
        domConstruct.create('div',
                            {id:'visitHomeContentPane'},
                            registry.byId('centerTopTabPane').domNode,
                            'last');

        var visitPane = new ContentPane({id       : "visitHomeContentPane",
                                         closable : true,
                                         disabled : false,
                                         selected : true
                                        },
                                        'visitHomeContentPane'
                                       );
        main_tab_container.addChild(visitPane);

      }

      else{
        console.log("Visit Tab already present.. so not creating. Selecting the same..");
        var visit_tab  = registry.byId('visitHomeContentPane');
        visit_tab.set('disabled',false);
        main_tab_container.selectChild(visit_tab);
      }

      fillTabWithDomAndDijits();
    }

    function fillTabWithDomAndDijits(){
      // Fill the Tab with appropriate Dom and Dijits
      console.log("Starting to fill contents into visit tab....");

      domConstruct.create('div',{id: "visitPaneContentBorderContainer",style: "height: 100%; width: 100%"},'visitHomeContentPane','first');
      domConstruct.create('div',{id: "visitPaneLSidebar", style: "height: 100%; width: 20em"},'visitPaneContentBorderContainer',0);
      domConstruct.create('div',{id: "visitPaneContentArea" /*, style: "height: 100%; width: 100em"*/},'visitPaneContentBorderContainer',1);

      console.log("created the DOMS");

      var visitPaneContentBorderContainer = new BorderContainer({id:"visitPaneContentBorderContainer"});
      var visitLSidebar    = new ContentPane({id       : "visitLSidebar",region: 'leading', splitter:true},
                                        'visitLSidebar'
                                       );
      var visitContentArea = new ContentPane({id       : "visitContentArea", region: 'center'},
                                        'visitContentArea'
                                       );
      console.log("created the Dijits");

      var main_visit_tab = registry.byId('visitHomeContentPane');

      main_visit_tab.addChild(visitPaneContentBorderContainer);
        visitPaneContentBorderContainer.addChild(visitLSidebar);
        visitPaneContentBorderContainer.addChild(visitContentArea);
      console.log("added the Dijits");

       visitPaneContentBorderContainer.placeAt(dom.byId('visitPaneContentBorderContainer'));
       visitPaneContentBorderContainer.startup();

      console.log("Dijits Started...");
    }

    createOrSelectTab();

//  function fillTabWithDomAndDijits(){
//    // Fill the Tab with appropriate Dom and Dijits
//  }

  });
}