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

    var ADMISSION_PANE     = {

        thisPane     : registry.byId('admissionHomeContentPane'),

        initialized  : false, 

        repositioned : false,
       
        displayPatientName : function(){

                                  var topBarHTML = dom.byId('selected_patient_info').innerHTML;
                                  var topBarStyle = domAttr.get( dom.byId('selected_patient_info'), 'style' ); 

                                  dom.byId('admissionPaneTopbar').innerHTML = topBarHTML;
                                  domAttr.set( dom.byId('admissionPaneTopbar'), 'style' , topBarStyle);

        },

        menuBar      : false,

        constructor  : function(){

                          console.log("Entering constructor function: Starting to create / select admission tab as necessary...");

                          if(! this.initialized){
                            console.log("Admission Pane is not initialized..");

                            /*
                              if(!this.repositioned){
                                this.repositionSearchBar();
                              }
                            */

                            this.doms();
                            this.dijits();
                            this.displayPatientName();                            
                            this.initialized = true;

                            new buildAdmissionTree();
//                             console.log("Admission Sidebar Tree Done..");
                            /*
                              if(!this.menuBar){
                                this.menuBar = new buildAdmissionMenu();
                                console.log(this.menuBar);
                              }
                              console.log("Admission Menu done ..");
                            */

                            return ADMISSION_PANE;

                          }
                          else{

                            console.log("Admission Pane is already initialized..");
                            this.destroyPane();

                          }
        },

        destroyPane : function(){
                          console.log("Entering function to destroy Admission Pane");
                          if( registry.byId('centerTopTabPane').
                                  getIndexOfChild(registry.byId('admissionHomeContentPane')) != -1 
                            ){
                            registry.byId('centerTopTabPane').
                                        removeChild( registry.byId('admissionHomeContentPane') );
                            registry.byId('admissionHomeContentPane').destroyRecursive(false);
                            }
                          console.log("Destroyed Admission Pane");                  
                          //this.menuBar = false;
                          this.initialized = false;
                          console.log("Recreating the Admission Pane");
                          this.constructor();
        },

        onPatientChange: function(){
                                this.destroyPane();
        },

        onPatientDelete: function(){
                                this.destroyPane();
        },

        onAdmissionChange: function(){
                                this.destroyPane();
        },

        onAdmissionDelete: function(){
                                this.destroyPane();
        },

        doms: function(){ 
              // Fill the Tab with appropriate DOMS
                  console.log("Entering Function to create Admision Tab DOMS ");

                  if(! dom.byId('admissionHomeContentPane')){
                      console.log("No DOMS in place. Creating the same...");
                      domConstruct.create('div',
                                          {id:'admissionHomeContentPane'},
                                          'centerTopTabPane',
                                          'last');

                      domConstruct.create('div',
                                          {id    : "admissionPaneContentBorderContainer",
                                            style : "height: 100%; width: 100%"
                                          },
                                          'admissionHomeContentPane',
                                          0);

                        domConstruct.create('div',      
                                            {id    : "admissionPaneTopbar"
                                            },
                                            'admissionPaneContentBorderContainer',
                                            0);

                        domConstruct.create('div',
                                            {id    : "admissionPaneLSidebar", 
                                              style : "height: 100%; width: 20em"
                                            },
                                            'admissionPaneContentBorderContainer',
                                            1);
                          domConstruct.create('div',
                                              {id    : "admissionLSidebarTreeContainer", 
                                                style : "height: 100%; width: 20em"
                                              },
                                              'admissionPaneLSidebar',
                                              0);
                            domConstruct.create('div',
                                              {id    : "admissionLSidebarTreeDiv", 
                                                style : "height: 100%; width: 20em"
                                              },
                                              'admissionLSidebarTreeContainer',
                                              0);

                        domConstruct.create('div',
                                            {id: "admissionPaneContentArea" 
                                            },
                                            'admissionPaneContentBorderContainer',
                                            2);

                      console.log("created the DOMS");
                      return dom.byId('admissionHomeContentPane');
                  }else{
                    console.log("DOMS already Present. Not creating them.");
                    return dom.byId('admissionHomeContentPane');
                  }
        },

        dijits: function(){
                      console.log("Entering function to create Admission pane Dijits");
                      
                      if(! registry.byId('admissionHomeContentPane')){
                        console.log("No Admission pane dijits present, creating the same");
                        var centerTopTabPane = registry.byId('centerTopTabPane');
                        console.log(centerTopTabPane);

                        var admissionHomeContentPane = new ContentPane({id        : 'admissionHomeContentPane',
                                                                        title     : 'Admissions',
                                                                        closable : false
                                                                       },
                                                                       'admissionHomeContentPane'
                                                      );
                        console.log("Trying to add AdmissionHomePane");
                        centerTopTabPane.addChild(admissionHomeContentPane,1);
                        console.log(admissionHomeContentPane);

                        var admissionPaneContentBorderContainer = new BorderContainer({id:"admissionPaneContentBorderContainer"
                                                                                      }, 
                                                                                      'admissionPaneContentBorderContainer');
                        admissionHomeContentPane.addChild(admissionPaneContentBorderContainer);
                        console.log(admissionPaneContentBorderContainer);

                        var admissionPaneTopbar    = new ContentPane({id        : "admissionPaneTopbar",
                                                                      region    : 'top', 
                                                                      splitter  : false
                                                                    },
                                                                    'admissionPaneTopbar'
                                                        );
                        admissionPaneContentBorderContainer.addChild(admissionPaneTopbar);
                        console.log(admissionPaneTopbar);

                        var admissionPaneLSidebar    = new ContentPane({id        : "admissionPaneLSidebar",
                                                                        region    : 'leading', 
                                                                        splitter  : true
                                                                        },
                                                                        'admissionPaneLSidebar'
                                                  );
                        admissionPaneContentBorderContainer.addChild(admissionPaneLSidebar);
                        console.log(admissionPaneLSidebar);

                        var admissionPaneContentArea = new ContentPane({id        : "admissionPaneContentArea", 
                                                                        region    : 'center',
                                                                        splitter  : true,
                                                                        gutters   : true
                                                                  },
                                                                  'admissionPaneContentArea'
                                                        );
                        admissionPaneContentBorderContainer.addChild(admissionPaneContentArea);
                        console.log(admissionPaneContentArea);

                        console.log("created the Dijits");
                        console.log("added the Dijits");

                        admissionHomeContentPane.startup();
                        centerTopTabPane.resize();

                        console.log("Dijits Started...");
                        return registry.byId('admissionHomeContentPane');

                      }else{
                        console.log("Admission Pane dijits already present. No recreating");
                        return registry.byId('admissionHomeContentPane');
                      }
        }

  };
  
  return ADMISSION_PANE;
  
  });