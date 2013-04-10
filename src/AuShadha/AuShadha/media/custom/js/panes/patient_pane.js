define(['dojo/dom',
         'dojo/dom-construct',
         'dojo/dom-style',
         'dojo/on',
         'dojo/json',
         'dojo/_base/array',
         'dijit/registry',
         'dijit/layout/BorderContainer',
         'dojox/layout/ContentPane',
         'dijit/layout/TabContainer',
         'dijit/form/FilteringSelect',

         "dojo/parser",

        "dojox/grid/DataGrid",
        "dojo/store/JsonRest",
        "dojo/data/ObjectStore",
        "dojo/request/xhr", 
        "dojo/json",

       'aushadha/panes/event_controller',

        'dojo/domReady!'
],
function(dom,
         domConstruct,
         domStyle,
         on,
         JSON, 
         array,
         registry, 
         BorderContainer,
         ContentPane,
         TabContainer,
         FilteringSelect,
         
         parser,
         DataGrid,
         JsonRest,
         ObjectStore,
         xhr,
         JSON,
         auPaneEventController
         
        ){

      var PATIENT_PANE = {

        initialized: false,

        repositioned: false,

        repositionSearchBar: function(){
                  if(! this.repositioned){
                    domConstruct.destroy('frontPageSearchPatientAuShadhaLogo');
                    console.log("Destroyed the logo....first..")
                    domStyle.set(
                                dom.byId('searchPatientContainerDiv'),
                                 {top           : "0px",
                                  left          : "0px",
                                  height        : "50px",
                                  width         : "auto",
                                  background    : "none",
                                  border        : "none",
                                  'boxShadow'   : "none",
                                  "borderRadius": "none",
                                  'fontSize'    : "inherit",
                                  "padding"     : "0px 0px 10px 0px;",
                                  overflow      : 'hidden',
                                  "margin"      : "0px 0px 10px 0px;",
                                  "display"     : "none"
                                });
                    domStyle.set(
                                dom.byId('searchTitle'),
                                        {top:"0px",left:"0px"}
                                );
                    registry.byId('addPatientButton').
                              set('iconClass',"addPatientIcon_16");
                    domStyle.set(
                                dom.byId('simplePatientFilteringSearch'),
                                 {top          : "0px",
                                  left          : "0px",
                                  overflow      : 'hidden',
                                  height        : "50px",
                                  width         : "auto",
                                  background    : "none",
                                  border        : "none",
                                  'boxShadow'   : "none",
                                  "borderRadius": "none",
                                  'fontSize'    : "inherit",
                                  "padding"     : "0px 0px 10px 0px;",
                                  "margin"      : "0px 0px 10px 0px;"
                                  });

                    registry.byId('addPatientButton').
                              set("style", 
                                  {"fontSize": "12px"} 
                              );
                    registry.byId('filteringSelectPatSearch').
                              set("style",
                                   {width     : "400px", 
                                    left      : "5%", 
                                    "fontSize": "12px"
                                   } 
                                 );
                    this.repositioned = true;
                  }
                  else{
                    return;
                  }
        },

        doms: function(){

                console.log("Creating the necessary Patient Pane DOMS ")

                if(!dom.byId('patientTabsBorderContainer') ){
                  domConstruct.create('div',
                                        {id: "patientTabsBorderContainer"},
                                        "patientMainContainer",
                                        "first"
                  );
                }

                if( !dom.byId('patientSidebarContentPane')){
                  domConstruct.create('div',
                                        {id: "patientSidebarContentPane"},
                                        "patientTabsBorderContainer",
                                        0
                  );
                    domConstruct.create('div',
                                        {id: "patientSidebarTabContainer"},
                                        "patientSidebarContentPane",
                                        "first"
                    );

                      domConstruct.create('div',
                                          {id: "patientTreeContainer"},
                                          "patientSidebarTabContainer",
                                          "first"
                      );
                        domConstruct.create('div',
                                            {id: "patientTreeDiv"},
                                            "patientTreeContainer",
                                            "first"
                        );

                      domConstruct.create('div',
                                          {id: "patientSidebarDiv_media"},
                                          "patientTreeContainer",
                                          "after"
                      );
                }

                if(! dom.byId('patientContextContainer')){
                  domConstruct.create('div',
                                  {id: 'patientContextContainer'},
                                  'patientTabsBorderContainer',
                                  1
                                );
                  domConstruct.create('div',
                                  {id: 'patientContextTabs'},
                                  'patientContextContainer',
                                  'first'
                                );
                    domConstruct.create('div',
                                        {id: 'patientSummaryTab'},
                                        'patientContextTabs',
                                        'first'
                                      );
                    domConstruct.create('div',
                                        {id: 'patientSynopsisBorderContainer'},
                                        'patientSummaryTab',
                                        'first'
                                      );
                    domConstruct.create('div',
                                        {id: 'patientSynopsisTopContentPane'},
                                        'patientSynopsisBorderContainer',
                                        'first'
                                      );
                }
                console.log("Created Patient Pane DOMS");
                this.setStyles();
        },

        setStyles: function(){
                console.log("Setting Styles for Patient Pane DOMS");

                domStyle.set(dom.byId('patientTabsBorderContainer'),
                             {"height"  : "50em",
                              "width"    : "100em",
                              "overflow" : "auto"
                             });
                domStyle.set( dom.byId('patientSidebarContentPane'),
                              {'minWidth' : '17em',
                              'minHeight' : "400px",
                              'overflow'  : "auto"
                });

                domStyle.set( dom.byId('patientTreeContainer'),
                              {'minWidth' : '17em',
                              'minHeight' : "400px",
                              'overflow'  : "auto"
                });

                  domStyle.set( dom.byId('patientTreeDiv'),
                                {'minWidth' : '17em',
                                'minHeight' : "15em",
                                'overflow'  : "auto",
                                "display"   : "block"
                  });
                domStyle.set( dom.byId('patientSidebarDiv_media'),
                              {'minWidth' : '275px',
                              'minHeight' : "400px",
                              'overflow'  : "auto"
                });
                console.log("Styling of Patient Pane DOMS done");
        },

        menuBar: false,

        dijits: function(){

                    console.log("Setting Patient Pane Dijits");

                    if (! registry.byId('patientTabsBorderContainer') ){
                      var mainBorderContainer = new BorderContainer({id: 'patientTabsBorderContainer'},
                                                                    'patientTabsBorderContainer'
                                                                    );
                      registry.byId('patientMainContainer').addChild(mainBorderContainer);
//                       mainBorderContainer.startup();
                    }
                    else{
                      var mainBorderContainer = registry.byId("patientTabsBorderContainer");
                    }
                    
                    console.log("mainBorderContainer is: ");
                    console.log(mainBorderContainer);
                    
                    console.log( registry.byId('patientSidebarContentPane'));

                    var sideBarContentPane = new ContentPane({id       : "patientSidebarContentPane",
                                                              region   : "leading",
                                                              splitter : true,
                                                              style    : "width:18em;"
                                                          },
                                                        "patientSidebarContentPane"
                    );
                    mainBorderContainer.addChild(sideBarContentPane);
                    console.log("Added Sidebar Tree Container");
                    console.log(sideBarContentPane);

                      var sideBarTabContainer = new TabContainer({id    : "patientSidebarTabContainer",
                                                            tabStrip    : true,
                                                            tabPosition :'bottom',
                                                            },
                                                          "patientSidebarTabContainer"
                      );
                      sideBarContentPane.addChild(sideBarTabContainer)
                      console.log("Added Sidebar Tab Container");
                      console.log(sideBarTabContainer);

                        var sideBarTreeContainer = new ContentPane({id      : "patientTreeContainer",
                                                                  title     : "Tree",
                                                                  iconClass : "navigationIcon",
                                                                  showTitle : false,
                                                                  toolTip   : "Patient Tree"
                                                              },
                                                            "patientTreeContainer"
                        );
                        sideBarTabContainer.addChild(sideBarTreeContainer);
                        console.log("Added Sidebar Tree Container");
                        console.log(sideBarTreeContainer);

                        var sideBarMediaContainer = new ContentPane({id         : "patientSidebarDiv_media",
                                                                    title       : "Media",
                                                                    iconClass   : "mediaIcon",
                                                                    showTitle   : false,
                                                              },
                                                            "patientSidebarDiv_media"
                        );
                        sideBarTabContainer.addChild(sideBarMediaContainer);  
                        console.log("Added Sidebar Media Container");
                        console.log(sideBarMediaContainer);

                    var patientContextContainer = new ContentPane({id       : 'patientContextContainer', 
                                                        region    : "center",
                                                        splitter  : true,
                                                        gutters   : true
                                                        },
                                          'patientContextContainer'
                                        );
                    mainBorderContainer.addChild(patientContextContainer);
                    console.log("Added patientContextContainer");
                    console.log(patientContextContainer);

                      var mainTabs = new TabContainer({id          : 'patientContextTabs',
                                                    tabPosition  : 'top',
                                                    tabStrip     : true
                                                    },
                                            'patientContextTabs'
                                          );
                      patientContextContainer.addChild(mainTabs);
                      console.log("Added mainTabs");
                      console.log(mainTabs);

                        var summaryTab = new ContentPane({id: 'patientSummaryTab',
                                                        title: 'Synopsis',
                                                        closable:false
                                                        },
                                                'patientSummaryTab'
                                              );
                        mainTabs.addChild(summaryTab);
                        console.log("Added summaryTab");
                        console.log(summaryTab);

                          var topBorderContainer = new BorderContainer({id: 'patientSynopsisBorderContainer'},
                                                  'patientSynopsisBorderContainer'
                                                );
                          summaryTab.addChild(topBorderContainer);
                          console.log("Added  topBorderContainer");
                          console.log(topBorderContainer);

                            var topContentPane = new ContentPane({id: 'patientSynopsisTopContentPane', 
                                                                region: 'center'},
                                                    'patientSynopsisTopContentPane'
                                                  );
                            topBorderContainer.addChild(topContentPane);
                            console.log("Added topContentPane");
                            console.log(topContentPane);

            sideBarContentPane.startup();
            patientContextContainer.startup();

            mainBorderContainer.startup();
            mainBorderContainer.resize();

            console.log("Created Patient Pane Dijits");

        },

        constructor : function(){
                      console.log("Entering the Constructor function for Patient Pane");
                      if(!this.initialized){
                        console.log("Patient Pane is not initialized..");
                        if(!this.repositioned){
                          this.repositionSearchBar();
                        }
                        this.doms();
                        this.dijits();
                        this.initialized = true;
                        new buildPatientTree();
                        console.log("Patient Sidebar Tree Done..")
                        /*
                          if(!this.menuBar){
                            this.menuBar = new buildPatientMenu();
                            console.log(this.menuBar);
                          }
                          console.log("Patient Menu done ..")
                        */
                          return PATIENT_PANE;
                      }
                      else{
                        console.log("Patient Pane is already initialized..");
                        this.destroyPane();
                      }
        },  

        destroyPane : function(){
                  console.log("Entering function to destroy Patient Pane");
                  registry.byId('patientTabsBorderContainer').destroyRecursive();
                  console.log("Destroyed Patient Pane");                  
                  //this.menuBar = false;
                  this.initialized = false;
                  console.log("Recreating the Patient Pane");
                  this.constructor();                  
        },

        onPatientDelete : function(){
          this.constructor();
        },

        onPatientUpdate : function(){
          this.constructor();
        },

        onPatientSwitch : function(){
          this.constructor();
        },
        
        setupPatientSummary: function (DivId, url){

                console.log("Filling DOM: " + DivId + " with URL: " + url);
                registry.byId(DivId).set('href',url);

               /*
                  xhr(url,{
                      handleAs: "text",
                      method  : "GET",
                  }).then(
                    function(json){
                        var jsondata = JSON.parse(json)
                        console.log(jsondata);
                        if(jsondata.success == true){
                          registry.byId("patientSummaryTab").set('href',url)        
                        }
                    },
                    function(json){
                          var jsondata = JSON.parse(json);
                          errorDialog.set("title", "ERROR");
                          errorDialog.set("content", jsondata.error_message);
                          errorDialog.show();
                    },
                    function(evt){console.log("Adding Data Finished Successfully...")}
                  );
                  console.log("Finished creating Patient Summary");
                  });
              */
              },
            searchWidget : function(){
                            var widgetStore = new JsonRest({target: PAT_SEARCH_JSON_URL});

                            /*
                              domStyle.set('filteringSelectPatSearchSmall',
                                          {width      : '250px'     ,
                                            height     : '18px'     ,
                                            margin     : 'none'     ,
                                            padding    : 'none'     ,
                                            position   : 'relative' ,
                                            top        : '-3.0em'   ,
                                            marginLeft : '10px'
                              });
                            */

                            var searchBox = new FilteringSelect({regExp        : '[a-zA-Z0-9 -]+'  ,
                                                                required       : true              ,
                                                                invalidMessage : 'No Results'      ,
                                                                store          : widgetStore       ,
                                                                searchAttr     : 'name'            ,
                                                                labelAttr      : 'label'           ,
                                                                labelType      : 'html'            ,
                                                                autoComplete   : false             ,
                                                                placeHolder    : 'Patient\'s Name' ,
                                                                hasDownArrow   : false             ,
                                                                onChange       : function(e){
                                                                                    try{
                                                                                      auPaneEventController.onPatientChoice(e);
                                                                                    }catch(err){
                                                                                      console.error(err.message);
                                                                                    }
                                                                                 },
                                                                style          : 'width:160%; textAlign:center;'
                                                                },
                                                                'filteringSelectPatSearch');

                            searchBox.startup();
            }
      };

//       PATIENT_PANE.searchWidget();
      return PATIENT_PANE;
});