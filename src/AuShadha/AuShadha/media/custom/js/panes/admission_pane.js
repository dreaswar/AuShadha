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

//     var main_tab_container = registry.byId("centerTopTabPane");

    var ADMISSION_PANE     = {

        thisPane     : registry.byId('admissionHomeContentPane'),

        initialized  : false, 

        repositioned : false,
       
        displayPatientName : function(){
                                  var topBarHTML = dom.byId('selected_patient_info').innerHTML;
                                  dom.byId('admissionPaneTopbar').innerHTML = topBarHTML;
        },

        menuBar      : false,

        constructor  : function(){

                          console.log("Starting to create / select admission tab as necessary...");

                          if(!this.initialized){
                            console.log("Admission Pane is not initialized..");

                            /*
                              if(!this.repositioned){
                                this.repositionSearchBar();
                              }
                            */
//                          this.displayPatientName();

                            this.doms();
                            this.dijits();
                            this.initialized = true;
                            new buildAdmissionTree();

                            console.log("Admission Sidebar Tree Done..");

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
                          registry.byId('admissionHomeContentPane').destroyRecursive();
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
                  console.log("Starting to fill contents into admission tab....");
                  if(! dom.byId('admissionHomeContentPane')){
                      domConstruct.create('div',
                                          {id:'admissionHomeContentPane'},
                                          'centerTopTabPane',
                                          'last');

                      domConstruct.create('div',
                                          {id    : "admissionPaneContentBorderContainer",
                                            style : "height: 100%; width: 100%"
                                          },
                                          'admissionHomeContentPane',
                                          'first');

                      domConstruct.create('div',
                                          {id    : "admissionPaneLSidebar", 
                                            style : "height: 100%; width: 20em"
                                          },
                                          'admissionPaneContentBorderContainer',
                                          0);

                      domConstruct.create('div',
                                          {id: "admissionPaneContentArea" 
                                          /*, style: "height: 100%; width: 100em"*/
                                          },
                                          'admissionPaneContentBorderContainer',
                                          1);

                      console.log("created the DOMS");
                  }
                  else{
                    console.log("DOMS already Present...");
                  }
        },

        dijits: function(){
                      var centerTopTabPane = registry.byId('centerTopTabPane');
                      var admissionHomeContentPane = new ContentPane({id        : 'admissionHomeContentPane',
                                                                      title     : 'Admissions'
                                                                      },
                                                                     'admissionHomeContentPane'
                                                     );

                      centerTopTabPane.addChild(admissionHomeContentPane);

                      var admissionPaneContentBorderContainer = new BorderContainer({id:"admissionPaneContentBorderContainer"}, 
                                                                                    'admissionPaneContentBorderContainer');
                      admissionHomeContentPane.addChild(admissionPaneContentBorderContainer);

                      var admissionLSidebar    = new ContentPane({id       : "admissionLSidebar",
                                                                region    : 'leading', 
                                                                splitter  : true
                                                                },
                                                                'admissionLSidebar'
                                                );
                      admissionPaneContentBorderContainer.addChild(admissionLSidebar);

                      var admissionContentArea = new ContentPane({id     : "admissionContentArea", 
                                                                  region : 'center',
                                                                 splitter  : true,
                                                                 gutters : true
                                                                },
                                                                'admissionContentArea'
                                                      );
                      admissionPaneContentBorderContainer.addChild(admissionContentArea);
                      console.log("created the Dijits");

//                       main_tab_container.startup();

                      console.log("added the Dijits");

//                    admissionPaneContentBorderContainer.placeAt(dom.byId('admissionPaneContentBorderContainer'));
//                    admissionPaneContentBorderContainer.startup();
                      console.log("Dijits Started...");
        }

  };
  
  return ADMISSION_PANE;
  
  });