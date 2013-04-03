define(
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
  function(registry,
           parser, 
           BorderContainer,
           TabContainer, 
           ContentPane, 
           /*ExpandoPane,*/ 
           Editor,
           Button,
           dom, 
           domConstruct, 
           domStyle, 
           ready,
           array,
           xhr
  ){

    var main_tab_container = registry.byId("centerTopTabPane");

    var VISIT_PANE     = {

        thisPane     : registry.byId('visitHomeContentPane'),

        initialized  : false, 

        repositioned : false,
       
        displayPatientName : function(){
                                  var topBarHTML = dom.byId('selected_patient_info').innerHTML;
                                  dom.byId('visitPaneTopbar').innerHTML = topBarHTML;
        },

        menuBar      : false,

        constructor  : function(){

                          console.log("Starting to create / select visit tab as necessary...");

                          if(!this.initialized){
                            console.log("Visit Pane is not initialized..");
                            /*
                            if(!this.repositioned){
                              this.repositionSearchBar();
                            }
                            */
                            this.displayPatientName();
                            this.doms();
                            this.dijits();
                            this.initialized = true;
                            new buildVisitTree();

                            console.log("Visit Sidebar Tree Done..");

                            /*
                              if(!this.menuBar){
                                this.menuBar = new buildVisitMenu();
                                console.log(this.menuBar);
                              }
                              console.log("Visit Menu done ..");
                            */

                            return VISIT_PANE;

                          }
                          else{
                            console.log("Visit Pane is already initialized..");
                            this.destroyPane();
                          }
        },

        destroyPane : function(){
                          console.log("Entering function to destroy Visit Pane");
                          registry.byId('visitHomeContentPane').destroyRecursive();
                          console.log("Destroyed Visit Pane");                  
                          //this.menuBar = false;
                          this.initialized = false;
                          console.log("Recreating the Visit Pane");
                          this.constructor();
        },

        onPatientChange: function(){
                                this.destroyPane();
        },

        onPatientDelete: function(){
                                this.destroyPane();
        },

        onVisitChange: function(){
                                this.destroyPane();
        },

        onVisitDelete: function(){
                                this.destroyPane();
        },

        doms: function(){ 
              // Fill the Tab with appropriate DOMS
                    console.log("Starting to fill contents into visit tab....");
                  if(! dom.byId('visitHomeContentPane')){
                      domConstruct.create('div',
                                          {id:'visitHomeContentPane'},
                                          registry.byId('centerTopTabPane').domNode,
                                          'last');

                      domConstruct.create('div',
                                          {id    : "visitPaneContentBorderContainer",
                                            style : "height: 100%; width: 100%"
                                          },
                                          'visitHomeContentPane',
                                          'first');
                      domConstruct.create('div',
                                          {id    : "visitPaneLSidebar", 
                                            style : "height: 100%; width: 20em"
                                          },
                                          'visitPaneContentBorderContainer',
                                          0);
                      domConstruct.create('div',
                                          {id: "visitPaneContentArea" 
                                          /*, style: "height: 100%; width: 100em"*/
                                          },
                                          'visitPaneContentBorderContainer',
                                          1);

                      console.log("created the DOMS");
                  }
                  else{
                    console.log("DOMS already Present...");
                  }
        },

        dijits: function(){
//                      var main_visit_tab = registry.byId('visitHomeContentPane');
                      var visitHomeContentPane = new ContentPane({title     : 'Visits',
                                                                      disabled  : false, 
                                                                      closable  : false
                                                                      },
                                                                     'visitHomeContentPane'
                                                     );

                      var visitPaneContentBorderContainer = new BorderContainer({id:"visitPaneContentBorderContainer"}, 
                                                                                    'visitPaneContentBorderContainer');

                      var visitLSidebar    = new ContentPane({id       : "visitLSidebar",
                                                                region    : 'leading', 
                                                                splitter  : true
                                                                },
                                                                'visitLSidebar'
                                                );
                      var visitContentArea = new ContentPane({id     : "visitContentArea", 
                                                                  region : 'center',
                                                                 splitter  : true,
                                                                 gutters : true
                                                                },
                                                                'visitContentArea'
                                                      );
                      console.log("created the Dijits");

                      main_tab_container.addChild(visitHomeContentPane);

                      visitHomeContentPane.addChild(visitPaneContentBorderContainer);
                        visitPaneContentBorderContainer.addChild(visitLSidebar);
                        visitPaneContentBorderContainer.addChild(visitContentArea);
                      visitHomeContentPane.startup();

                      console.log("added the Dijits");

//                    visitPaneContentBorderContainer.placeAt(dom.byId('visitPaneContentBorderContainer'));
//                    visitPaneContentBorderContainer.startup();
                      console.log("Dijits Started...");
        }

  };
  
  return VISIT_PANE;
  
  });