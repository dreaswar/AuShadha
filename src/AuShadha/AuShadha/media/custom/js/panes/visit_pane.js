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
   'dojo/dom-attr',
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
           domAttr,
           ready,
           array,
           xhr
  ){

//     var main_tab_container = registry.byId("centerTopTabPane");

    var VISIT_PANE     = {

        thisPane     : registry.byId('visitHomeContentPane'),

        initialized  : false, 

        repositioned : false,
       
        displayPatientName : function(){

                                  var topBarHTML = dom.byId('selected_patient_info').innerHTML;
                                  var topBarStyle = domAttr.get( dom.byId('selected_patient_info'), 'style' ); 

                                  dom.byId('visitPaneTopbar').innerHTML = topBarHTML;
                                  domAttr.set( dom.byId('visitPaneTopbar'), 'style' , topBarStyle);

        },

        menuBar      : false,

        constructor  : function(){

                          console.log("Entering constructor function: Starting to create / select visit tab as necessary...");

                          if(! this.initialized){
                            console.log("Visit Pane is not initialized..");

                            /*
                              if(!this.repositioned){
                                this.repositionSearchBar();
                              }
                            */

                            this.doms();
                            this.dijits();
                            this.displayPatientName();                            
                            this.initialized = true;

                            new buildVisitTree();
//                             console.log("Visit Sidebar Tree Done..");
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
                          if( registry.byId('centerTopTabPane').
                                  getIndexOfChild(registry.byId('visitHomeContentPane')) != -1 
                            ){
                            registry.byId('centerTopTabPane').
                                  removeChild( registry.byId('visitHomeContentPane') );
                            registry.byId('visitHomeContentPane').destroyRecursive(false);
                            }
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
                  console.log("Entering Function to create Visit Tab DOMS ");

                  if(! dom.byId('visitHomeContentPane')){
                      console.log("No DOMS in place. Creating the same...");
                      domConstruct.create('div',
                                          {id:'visitHomeContentPane'},
                                          'centerTopTabPane',
                                          'last');

                      domConstruct.create('div',
                                          {id    : "visitPaneContentBorderContainer",
                                            style : "height: 100%; width: 100%"
                                          },
                                          'visitHomeContentPane',
                                          0);

                        domConstruct.create('div',      
                                            {id    : "visitPaneTopbar"
                                            },
                                            'visitPaneContentBorderContainer',
                                            0);

                        domConstruct.create('div',
                                            {id    : "visitPaneLSidebar", 
                                              style : "height: 100%; width: 20em"
                                            },
                                            'visitPaneContentBorderContainer',
                                            1);
                          domConstruct.create('div',
                                              {id    : "visitLSidebarTreeContainer", 
                                                style : "height: 100%; width: 20em"
                                              },
                                              'visitPaneLSidebar',
                                              0);
                          domConstruct.create('div',
                                            {id    : "visitLSidebarTreeDiv", 
                                              style : "height: 100%; width: 20em"
                                            },
                                            'visitLSidebarTreeContainer',
                                            0);

                        domConstruct.create('div',
                                            {id: "visitPaneContentArea" 
                                            },
                                            'visitPaneContentBorderContainer',
                                            2);

                      console.log("created the DOMS");
                      return dom.byId('visitHomeContentPane');
                  }else{
                    console.log("DOMS already Present. Not creating them.");
                    return dom.byId('visitHomeContentPane');
                  }
        },

        dijits: function(){
                      console.log("Entering function to create Visit pane Dijits");
                      
                      if(! registry.byId('visitHomeContentPane')){
                        console.log("No Visit pane dijits present, creating the same");
                        var centerTopTabPane = registry.byId('centerTopTabPane');
                        console.log(centerTopTabPane);

                        var visitHomeContentPane = new ContentPane({id        : 'visitHomeContentPane',
                                                                        title     : 'Visits',
                                                                        closable : false
                                                                       },
                                                                       'visitHomeContentPane'
                                                      );
                        console.log("Trying to add VisitHomePane");
//                         debugger
                        centerTopTabPane.addChild(visitHomeContentPane,2);
//                         debugger
                        console.log(visitHomeContentPane);
//                         debugger
                        var visitPaneContentBorderContainer = new BorderContainer({id:"visitPaneContentBorderContainer"
                                                                                      }, 
                                                                                      'visitPaneContentBorderContainer');
                        visitHomeContentPane.addChild(visitPaneContentBorderContainer);
                        console.log(visitPaneContentBorderContainer);
                        
                        var visitPaneTopbar    = new ContentPane({id        : "visitPaneTopbar",
                                                                      region    : 'top', 
                                                                      splitter  : false
                                                                    },
                                                                    'visitPaneTopbar'
                                                        );
                        visitPaneContentBorderContainer.addChild(visitPaneTopbar);
                        console.log(visitPaneTopbar);

                        var visitPaneLSidebar    = new ContentPane({id        : "visitPaneLSidebar",
                                                                        region    : 'leading', 
                                                                        splitter  : true
                                                                        },
                                                                        'visitPaneLSidebar'
                                                  );
                        visitPaneContentBorderContainer.addChild(visitPaneLSidebar);
                        console.log(visitPaneLSidebar);

                        var visitPaneContentArea = new ContentPane({id        : "visitPaneContentArea", 
                                                                        region    : 'center',
                                                                        splitter  : true,
                                                                        gutters   : true
                                                                  },
                                                                  'visitPaneContentArea'
                                                        );
                        visitPaneContentBorderContainer.addChild(visitPaneContentArea);
                        console.log(visitPaneContentArea);

                        console.log("created the Dijits");
                        console.log("added the Dijits");

                        visitHomeContentPane.startup();
                        centerTopTabPane.resize();

                        console.log("Dijits Started...");
                        return registry.byId('visitHomeContentPane');

                      }else{
                        console.log("Visit Pane dijits already present. No recreating");
                        return registry.byId('visitHomeContentPane');
                      }
        }

  };
  
  return VISIT_PANE;
  
  });