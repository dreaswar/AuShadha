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
   "dojo/request"
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
           request
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
                            request(CHOSEN_PATIENT.visitsummary).then(
                              function(html){
//                                 registry.byId('visitPaneRSidebar').set('content',html);
                                registry.byId('visitSummaryTab').set('content',html);
                              },
                              function(err){
                                publishError(err);
                              }
                            );
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
//                           registry.byId('visitPaneRSidebar').set('href',CHOSEN_PATIENT.visitsummary);
                          registry.byId('visitSummaryTab').set('href',CHOSEN_PATIENT.visitsummary);
                          new buildVisitTree();
                          new buildPatientTree();
                          new buildAdmissionTree();
                          this.destroyPane();
        },

        onVisitDelete: function(){
                          registry.byId('visitSummaryTab').set('href',CHOSEN_PATIENT.visitsummary);                
//                           registry.byId('visitPaneRSidebar').set('href',CHOSEN_PATIENT.visitsummary);                
                          this.destroyPane();
        },

        addPane : {

          doms: function(nodeId){
                      if(!dom.byId(this.nodeId)){
                        domConstruct.create('div',
                                          {id:this.nodeId},
                                          'visitEditPaneTabContainer',
                                          'last');
                      }
                      console.log("Created a Add pane DOMS");
          },

          dijits: function(nodeId){
                      console.log("Creating a Add pane Dijit");
                      var visitAddTab = new ContentPane({id      : this.nodeId,
                                                        closable : true},
                                                        nodeId);
                      registry.byId('visitEditPaneTabContainer').addChild(visitAddTab);
                      visitAddTab.startup();
          },

          destroyPane: function(nodeId){
                        if(this.initialized(this.nodeId)){
                          registry.byId(this.nodeId).destroyRecursive();
                        }
                        this.constructor({id: this.nodeId, 
                                         title: this.nodeTitle,
                                         content:this.nodeContent});
          },

          constructor : function(obj){
                          console.log("Calling constructor method to addVisitPane");
                          this.nodeId      = obj.id[0];
                          this.nodeTitle   = obj.title;
                          this.nodeContent = obj.content;
                          console.log(obj);
                          if(! this.initialized(this.nodeId)){
                            this.doms(this.nodeId);
                            this.dijits(this.nodeId);
                          }
                          this.widget      = registry.byId(this.nodeId);
                          registry.byId('visitEditPaneTabContainer').selectChild(this.widget);
                          this.widget.set('title',this.nodeTitle);
                          this.widget.set('content',this.nodeContent);
                          return this.widget;
          },

          initialized : function(nodeId){
                        if(registry.byId(this.nodeId)){
                          return true;
                        }
                        else{
                          return false;
                        }
          }

        },

       editPane : {

          doms: function(nodeId){
                      if(!dom.byId(nodeId) ){
                        domConstruct.create('div',
                                            {id:nodeId},
                                            'visitEditPaneTabContainer',
                                            'last');
                      }
          },

          dijits: function(nodeId){
                      var visitEditTab = new ContentPane({id     : nodeId,
                                                        closable : true},
                                                        nodeId);
                      registry.byId('visitEditPaneTabContainer').addChild(visitEditTab);
                      visitEditTab.startup();
          },

          destroyPane: function(nodeId){
                        if(this.initialized(nodeId)){
                          registry.byId(nodeId).destroyRecursive();
                        }
                        this.constructor(nodeId);
          },

          constructor : function(obj){
                          var nodeId      = "visitEditTab_"+ obj.id;
                          var nodeTitle   = obj.title;
                          var nodeContent = obj.content;

                          if(! this.initialized(nodeId)){
                            this.doms(nodeId);
                            this.dijits(nodeId);
                          }
                          registry.byId('visitEditPaneTabContainer').selectChild(nodeId);
                          registry.byId(nodeId).set('title',nodeTitle);
                          registry.byId(nodeId).set('content',nodeContent);
                          return registry.byId(nodeId);
          },

          initialized : function(nodeId){
                        if( registry.byId(nodeId) ){
                          return true;
                        }
                        else{
                          return false;
                        }
          }

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
                                              {id    : "visitLSidebarTabContainer", 
                                                style : "height: 100%; width: 20em"
                                              },
                                              'visitPaneLSidebar',
                                              0);
                            domConstruct.create('div',
                                                {id    : "visitLSidebarTreeContainer", 
                                                  style : "height: 100%; width: 20em"
                                                },
                                                'visitLSidebarTabContainer',
                                                0);
                              domConstruct.create('div',
                                                {id    : "visitLSidebarTreeDiv", 
                                                  style : "height: 100%; width: 20em"
                                                },
                                                'visitLSidebarTreeContainer',
                                                0);
                              
                            domConstruct.create('div',
                                              {id    : "visitSummaryContainer", 
                                                style : "height: 100%; width: 20em"
                                              },
                                              'visitLSidebarTabContainer',
                                              1);

                        domConstruct.create('div',
                                            {id: "visitPaneContentArea" 
                                            },
                                            'visitPaneContentBorderContainer',
                                            2);

                          domConstruct.create('div',
                                              {id: 'visitEditPaneTabContainer'},
                                              'visitPaneContentArea',
                                              'first');
                            domConstruct.create('div',
                                                {id: 'visitSummaryTab'},
                                                'visitEditPaneTabContainer',
                                                0);

                        /*                          
                            domConstruct.create('div',
                                                {id: 'visitEditPane'},
                                                'visitEditPaneTabContainer',
                                                'first');
                        */

                        /*
                        domConstruct.create('div',
                                            {id: "visitPaneRSidebar" 
                                            },
                                            'visitPaneContentBorderContainer',
                                            3);
                        */
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

                          var visitLSidebarTabContainer = new TabContainer({id    : "visitLSidebarTabContainer",
                                                                tabStrip    : true,
                                                                tabPosition :'bottom',
                                                                },
                                                              "visitLSidebarTabContainer"
                          );
                          visitPaneLSidebar.addChild(visitLSidebarTabContainer)
                          console.log("Added Sidebar Tab Container");
                          console.log(visitLSidebarTabContainer);

                            var visitLSidebarTreeContainer = new ContentPane({id      : "visitLSidebarTreeContainer",
                                                                      title     : "Tree",
                                                                      iconClass : "navigationIcon",
                                                                      showTitle : false,
                                                                      toolTip   : "OPD Visit Tree"
                                                                  },
                                                                "visitLSidebarTreeContainer"
                            );
                            visitLSidebarTabContainer.addChild(visitLSidebarTreeContainer);
                            console.log("Added Sidebar Tree Container");
                            console.log(visitLSidebarTreeContainer);

                            var visitSummaryContainer = new ContentPane({id       : "visitSummaryContainer",
                                                                      title     : "Visit Notes",
                                                                      iconClass : "mediaIcon",
                                                                      showTitle : false,
                                                                },
                                                              "visitSummaryContainer"
                            );
                            visitLSidebarTabContainer.addChild(visitSummaryContainer);  
                            console.log("Added Visit Summary Container");
                            console.log(visitSummaryContainer);


                        var visitPaneContentArea = new ContentPane({id        : "visitPaneContentArea", 
                                                                    region    : 'center',
                                                                    splitter  : true,
                                                                    gutters   : true
                                                                  },
                                                                  'visitPaneContentArea'
                                                        );
                        visitPaneContentBorderContainer.addChild(visitPaneContentArea);
                        console.log(visitPaneContentArea);


                        var visitEditPaneTabContainer = new TabContainer({id  : 'visitEditPaneTabContainer', 
                                                                          tabStrip    : true, 
                                                                          tabPosition : 'top'},
                                                                          'visitEditPaneTabContainer'
                                                                        );
                        visitPaneContentArea.addChild(visitEditPaneTabContainer);

                        var visitSummaryTab = new ContentPane({id  : 'visitSummaryTab', 
                                                              title: "Synopsis", 
                                                              closable: false,
                                                              tabPosition : 'top'},
                                                              'visitSummaryTab'
                                                            );
                        visitEditPaneTabContainer.addChild(visitSummaryTab);

                        visitEditPaneTabContainer.startup();                        

                        /*                        
                        var visitEditPane             = new ContentPane({id      : 'visitEditPane',
                                                                        title    : "Edit Visit",
                                                                        content  : "Click a visit on tree to load it"
                                                                        },
                                                                        'visitEditPane');
                        visitEditPaneTabContainer.addChild(visitEditPane);                                

//                         console.log(visitEditPane);
//                         visitEditPane.startup();

                        */

                        /*
                        var visitPaneRSidebar = new ContentPane({id         : "visitPaneRSidebar", 
                                                                 region    : 'trailing',
                                                                 splitter  : true,
                                                                 gutters   : true,
                                                                 style     : "width      : 35em;    \
                                                                              background : #F5F9F4; \
                                                                              borders    : none;    \
                                                                              "
                                                                 },
                                                                 'visitPaneRSidebar'
                                                        );
                        visitPaneContentBorderContainer.addChild(visitPaneRSidebar);
                        */

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