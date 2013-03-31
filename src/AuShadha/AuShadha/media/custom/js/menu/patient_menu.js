function buildPatientMenu(){
  require(["dojo/ready", 
        "dijit/MenuBar",
        "dijit/PopupMenuBarItem", 
        "dijit/Menu",
        "dijit/MenuItem", 
        "dijit/DropDownMenu",
        "dijit/MenuBarItem",
        "dojo/dom",
        "dojo/dom-style",
        "dojo/dom-construct",
        "dijit/registry"
        ],
        function(ready, 
                  MenuBar, 
                  PopupMenuBarItem, 
                  Menu, 
                  MenuItem, 
                  DropDownMenu,
                  MenuBarItem,
                  dom,
                  domStyle,
                  domConstruct,
                  registry
                ){
              var pMenuBar = new MenuBar({});

              var pSynopsisLayout = new DropDownMenu({});
                pSynopsisLayout.addChild(new MenuItem({
                    label: "Default"
                }));
                pSynopsisLayout.addChild(new MenuItem({
                    label: "Portlets Only"
                }));
                pSynopsisLayout.addChild(new MenuItem({
                    label: "Tabbed Layout"
                }));

              var pAddMenu = new DropDownMenu({});

              pAddMenu.addChild(new MenuItem({
                    label     : "Neonatal History",
                    onClick   :  function(){
                                  require(["dojo/dom-construct",
                                          "dojo/dom-style",
                                          "dojox/layout/ContentPane",
                                          "dijit/registry","dojo/dom"],
                                    function(domConstruct,domStyle,ContentPane,registry,dom){
                                      var urlDict = {"neontalAndPaediatricExamUrl": CHOSEN_PATIENT.neonatalandpaediatricexamurl
                                      }
                                      if(!registry.byId('patientNeonatalAndPaediatricExamTab') ){
                                          console.log(CHOSEN_PATIENT);
                                          makeNeonatalAndPaediatricExamTab(urlDict);
                                      }
                                      else{
                                        registry.byId('patientContextTabs').selectChild(
                                          registry.byId('patientPreventiveHealthTab') )
                                        registry.byId("patientPreventiveTabs").selectChild(
                                          registry.byId("patientNeonatalAndPaediatricExamTab")
                                        );
                                      }
                                    }
                                  )
                    }
                }));

                pAddMenu.addChild(new MenuItem({
                  label     : "Obs.History",
                  onClick   : function(){
                                    require(
                                      ["dojo/dom-construct",
                                      "dojo/dom-style",
                                      "dojox/layout/ContentPane",
                                      "dijit/registry",
                                      "dojo/dom"],
                                    function(domConstruct,
                                            domStyle,
                                            ContentPane,
                                            registry,
                                            dom){
                                          var urlDict = {"obstetricHistoryUrl": CHOSEN_PATIENT.obstetrichistorydetailadd}
                                          if(!registry.byId('patientObstetricsPreventivesTab') ){
                                                  console.log(CHOSEN_PATIENT);
                                                  makeObstetricHistoryDetailTab(urlDict);
                                          }
                                          else{
                                              registry.byId('patientContextTabs').selectChild(
                                                  registry.byId('patientPreventiveHealthTab') )
                                              registry.byId("patientPreventiveTabs").selectChild(
                                                  registry.byId("patientObstetricsPreventivesTab")
                                              );
                                          }
                                    });
                               }
                }));

                pAddMenu.addChild(new MenuItem({
                    label: "Gyn.History",
                      onClick   :  function(){
                                  require(["dojo/dom-construct",
                                          "dojo/dom-style",
                                          "dojox/layout/ContentPane",
                                          "dijit/registry","dojo/dom"],
                                    function(domConstruct,domStyle,ContentPane,registry,dom){
                                      var urlDict = {"gynaecologyHistoryUrl": CHOSEN_PATIENT.gynaecologyhistorydetailadd
                                      }
                                      if(!registry.byId('patientGynaecologyPreventivesTab') ){
                                          console.log(CHOSEN_PATIENT);
                                          makeGynaecologyHistoryDetailTab(urlDict);
                                      }
                                      else{
                                        registry.byId('patientContextTabs').selectChild(
                                          registry.byId('patientPreventiveHealthTab') )
                                        registry.byId("patientPreventiveTabs").selectChild(
                                          registry.byId("patientGynaecologyPreventivesTab")
                                        );
                                      }
                                    }
                                  )
                    }
                }));

                pAddMenu.addChild(new MenuItem({
                    label: "Medical Preventives",
                    onClick   :  function(){
                                require(["dojo/dom-construct",
                                        "dojo/dom-style",
                                        "dojox/layout/ContentPane",
                                        "dijit/registry","dojo/dom"],
                                  function(domConstruct,domStyle,ContentPane,registry,dom){
                                    var urlDict = {"medicalPreventivesUrl": CHOSEN_PATIENT.medicalpreventivesadd
                                    }
                                    if(!registry.byId('patientMedicalPreventivesTab') ){
                                        console.log(CHOSEN_PATIENT);
                                        makeMedicalPreventivesTab(urlDict);
                                    }
                                    else{
                                      registry.byId('patientContextTabs').selectChild(
                                        registry.byId('patientPreventiveHealthTab') )
                                      registry.byId("patientPreventiveTabs").selectChild(
                                        registry.byId("patientMedicalPreventivesTab")
                                      );
                                    }
                                  }
                                )
                  }
                }));

                pAddMenu.addChild(new MenuItem({
                    label: "Surgical Preventives",
                    onClick   :  function(){
                                require(["dojo/dom-construct",
                                        "dojo/dom-style",
                                        "dojox/layout/ContentPane",
                                        "dijit/registry","dojo/dom"],
                                  function(domConstruct,domStyle,ContentPane,registry,dom){
                                    var urlDict = {"surgicalPreventivesUrl": CHOSEN_PATIENT.surgicalpreventivesadd
                                    }
                                    if(!registry.byId('patientSurgicalPreventivesTab') ){
                                        console.log(CHOSEN_PATIENT);
                                        makeSurgicalPreventivesTab(urlDict);
                                    }
                                    else{
                                      registry.byId('patientContextTabs').selectChild(
                                        registry.byId('patientPreventiveHealthTab') )
                                      registry.byId("patientPreventiveTabs").selectChild(
                                        registry.byId("patientSurgicalPreventivesTab")
                                      );
                                    }
                                  }
                                )
                  }
                }));

/*
              pMenuBar.addChild(new PopupMenuBarItem({
                  label     : "Customise",
                  title     : "Personalize Layout of Application",
                  popup     : pSynopsisLayout,
                  iconClass : "navigationIcon"
              }));
*/

              pMenuBar.addChild(new PopupMenuBarItem({
                  label: "Add-On Sheets",
                  title: "Add specific Speciality History and Preventive Info.",
                  popup: pAddMenu,
                  iconClass: "dijitEditorIcon dijitEditorIconCopy"
              }));

              /*
              pMenuBar.addChild(new MenuBarItem({
                  title     : "Contacts, Demographics and Insurance Info.",
                  label     : "Demographics",
                  onClick   :  function(){
                                require(["dojo/dom-construct",
                                          "dojo/dom-style",
                                          "dojox/layout/ContentPane",
                                          "dijit/registry","dojo/dom"],
                                function(domConstruct,domStyle,ContentPane,registry,dom){
                                  var urlDict = {demographicsUrl   : CHOSEN_PATIENT.demographicsadd,
                                                  contactUrl       : CHOSEN_PATIENT.contactjson,
                                                  phoneUrl         : CHOSEN_PATIENT.phonejson,
                                                  guardianUrl      : CHOSEN_PATIENT.guardianjson
                                                }
                                  if(!registry.byId('contactAndDemographicsTab') ){
                                        console.log(CHOSEN_PATIENT);
                                        makeDemographicsTab(urlDict);
                                  }
                                  else{
                                      registry.byId("patientContextTabs").selectChild(
                                          registry.byId("contactAndDemographicsTab")
                                      );
                                  }
                                })
                  }
              }));
              */

              pMenuBar.set("style",
                           {"position"   : "relative",
                            "float"      : "right",
              });

/*
              var pSubMenu2 = new DropDownMenu({});
              pSubMenu2.addChild(new MenuItem({
                  label: "Cut",
                  iconClass: "dijitEditorIcon dijitEditorIconCut"
              }));
              pSubMenu2.addChild(new MenuItem({
                  label: "Copy",
                  iconClass: "dijitEditorIcon dijitEditorIconCopy"
              }));
              pSubMenu2.addChild(new MenuItem({
                  label: "Paste",
                  iconClass: "dijitEditorIcon dijitEditorIconPaste"
              }));

              pMenuBar.addChild(new PopupMenuBarItem({
                  label: "Edit",
                  popup: pSubMenu2
              }));
*/

              if(registry.byId('patientMenuBar')){
                registry.byId('patientMenuBar').destroyRecursive();
              }

              if(! dom.byId('patientMenuBar') ){
                domConstruct.create('div',
                                  {'id':"patientMenuBar"},
                                  'patientTabsBorderContainer',
                                  'before'
                );
              }

              domStyle.set('patientMenuBar',
                            {'top'      : "2.3em",
                            "right"    : "1em",
                            "position" : "relative",
                            "zIndex"   : "1"
              });

              pMenuBar.placeAt('patientMenuBar');
              pMenuBar.startup();
              
              return pMenuBar;

//                  });
  });
}