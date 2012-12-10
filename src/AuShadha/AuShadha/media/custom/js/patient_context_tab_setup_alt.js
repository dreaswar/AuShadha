function patientContextTabSetup(){
require(
  ["dijit/registry",
   "dojo/parser",
   "dijit/layout/BorderContainer",
   "dijit/layout/TabContainer",
   "dojox/layout/ContentPane",
   "dijit/Editor",
   "dijit/form/Button",
   "dojo/dom",
   "dojo/dom-construct",
   "dojo/dom-style",
   "dojo/ready",
   "dojo/_base/array"
  ],
  function(registry,parser, BorderContainer,
           TabContainer, ContentPane, Editor,Button,
           dom, domConstruct, domStyle, ready,array
  ){
ready( function(){
      if (registry.byId("patientContextContainer")){
        console.log("Context Container already set up.. ")
        return;
      }
      else
      {
      console.log("No Content Panes set up so far.. setting the same..");

      domConstruct.destroy('frontPageSearchPatientAuShadhaLogo');
      domStyle.set(dom.byId('searchPatientContainerDiv'),{top           : "0px",
                                                          left          : "0px",
                                                          height        : "50px",
                                                          width         : "auto",
                                                          background    : "none",
                                                          border        : "none",
                                                          'boxShadow'   : "none",
                                                          "borderRadius": "none",
                                                          'fontSize'    : "inherit",
                                                          "padding"     : "0px 0px 10px 0px;",
                                                            overflow:'hidden',
                                                          "margin"      : "0px 0px 10px 0px;",
                                                          "display"     : "none"
                                                        });
      domStyle.set(dom.byId('searchTitle'),{top:"0px",left:"0px"});
      registry.byId('addPatientButton').set('iconClass',"addPatientIcon_16");
      domStyle.set(dom.byId('simplePatientFilteringSearch'),{top:"0px",
                                                            left:"0px",
                                                            overflow:'hidden',
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

      registry.byId('addPatientButton').set("style", {"fontSize": "12px"} );
      registry.byId('filteringSelectPatSearch').set("style",{width: "400px", left: "5%", "fontSize":"12px"} );

      domConstruct.create('div',
                          {id: "patientSidebarTabContainer"},
                          "patientTabsBorderContainer",
                          "first"
      );
        domConstruct.create('div',
                            {id: "patientSidebarContentPane"},
                            "patientTabsBorderContainer",
                            "first"
        );
          domConstruct.create('div',
                              {id: "patientTreeContainer"},
                              "patientSidebarTabContainer",
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
                                  {id: "patientSidebarDiv_allergy"},
                                  "patientTreeDiv",
                                  "after"
              );
                domConstruct.create('div',
                                    {id: "patientSidebarDiv_allergyHeader"},
                                    "patientSidebarDiv_allergy",
                                    "first"
                );
                domConstruct.create('div',
                                    {id: "patientSidebarDiv_allergyGridContainer"},
                                    "patientSidebarDiv_allergyHeader",
                                    "after"
                );
                  domConstruct.create('div',
                                  {id: "allergy_list"},
                                  "patientSidebarDiv_allergyGridContainer",
                                  "first"
                  );
            domConstruct.create('div',
                                {id: "patientSidebarDiv_contact"},
                                "patientTreeContainer",
                                "after"
            );
            domConstruct.create('div',
                                {id: "patientSidebarDiv_media"},
                                "patientSidebarDiv_contact",
                                "after"
            );
            domStyle.set( dom.byId('patientSidebarContentPane'),{'minWidth'  : '17em',
                                                                 'minHeight' : "400px",
                                                                 'overflow'  : "auto"
            });
            domStyle.set( dom.byId('patientTreeContainer'),{'minWidth' : '17em',
                                                            'minHeight': "400px",
                                                            'overflow' : "auto"
            });
            console.log("Created a Patient Tree Container..." + dom.byId("patientTreeContainer"));
              domStyle.set( dom.byId('patientTreeDiv'),{'minWidth' : '17em',
                                                        'minHeight': "15em",
                                                        'overflow' : "auto",
                                                        "display"  : "block"
              });
              domStyle.set( dom.byId('patientSidebarDiv_allergy'),{'minWidth' : '15em'  ,
                                                                  'minHeight': "15em"  ,
                                                                  'overflow' : "hidden"  ,
                                                                  "display"  : "block" ,
                                                                  "float"    : "left"  ,
                                                                  "position" : "absolute"     ,
                                                                  "bottom"   : "0.3em"        ,
                                                                  "border"   : "solid 1px #ddd",
                                                                  "padding"  : "0.4em",
                                                                  "background":"#CFE5FA"
              });
                domStyle.set( dom.byId('patientSidebarDiv_allergyHeader'),
                                                                    {'minWidth'       : '15em'  ,
                                                                    'height'         : "auto"  ,
                                                                    "display"        : "block" ,
                                                                    "float"          : "left"  ,
                                                                    "clear"          : "both" ,
                                                                    "position"       : "relative",
                                                                    "top"            : "0"        ,
                                                                    "padding"        : "1px",
                                                                    "background"     : "#2D285A",
                                                                    "color"          : "whitesmoke",
                                                                    "textAlign"      : "center",
                                                                    "verticalAlign"  : "middle",
                                                                    "fontWeight"     : "bold",
                                                                    "fontFamily"     : "dejavu sans"
                });
                  dom.byId("patientSidebarDiv_allergyHeader").innerHTML = "ALLERGY";
                domStyle.set( dom.byId('patientSidebarDiv_allergyGridContainer'),
                                                                    {'maxWidth'         : '15em'  ,
                                                                    'height'         : "auto"  ,
                                                                    "display"        : "block" ,
                                                                    "float"          : "left"  ,
                                                                    "clear"          : "both" ,
                                                                    "position"       : "relative",
                                                                    "top"            : "0"        ,
                                                                    "fontFamily"     : "dejavu sans"
                });
            domStyle.set( dom.byId('patientSidebarDiv_contact'),{'minWidth'  : '275px',
                                                                 'minHeight' : "400px",
                                                                 'overflow'  : "auto"
            });
            domStyle.set( dom.byId('patientSidebarDiv_media'),{'minWidth' : '275px',
                                                               'minHeight': "400px",
                                                               'overflow' : "auto"
            });

      domConstruct.create('div',
                          {id: "patientContextTabs"},
                          "patientContextContainer",
                          "first"
      );
      console.log("Created a PatientContextTabs..." + dom.byId("patientContextTabs"));

      console.log("Starting to set up individual tabs.. now creating domElements for the same");

      domConstruct.create('div',
                          {id: "patientSummaryTab"},
                         "patientContextTabs",
                         "first"
      );
        domConstruct.create('div',
                            {id: "patientSynopsisBorderContainer"},
                          "patientSummaryTab",
                          "first"
        );
        //domStyle.set( dom.byId('patientSynopsisBorderContainer'),{'minWidth':'100em','height':'100em','overflow':"auto"});
          domConstruct.create('div',
                              {id: "patientSynopsisTopContentPane"},
                            "patientSynopsisBorderContainer",
                            "first"
          );
          //domStyle.set( dom.byId('patientSynopsisTopContentPane'),{'width':'70em','height':'auto','overflow':"auto"});
            domConstruct.create('div',
                                {id: "medication_list"},
                                "patientSynopsisTopContentPane",
                                "first"
            );

          domConstruct.create('div',
                              {id: "patientSynopsisBottomContentPane"},
                            "patientSynopsisTopContentPane",
                            "after"
          );
//          domStyle.set( dom.byId('patientSynopsisBottomContentPane'),{'minWidth':'91em','minHeight':"75em",'overflow':"auto"});
            domConstruct.create('div',
                                {id: "patientSynopsisBottomTabContainer"},
                              "patientSynopsisBottomContentPane",
                              "first"
            );
              domConstruct.create('div',
                                {id: "patientSynopsisBottomContentPaneAdmissions"},
                              "patientSynopsisBottomTabContainer",
                              "first"
              );
                domConstruct.create('div',
                                  {id: "patientNewAdmissionNotes"},
                                  "patientSynopsisBottomContentPaneAdmissions",
                                  "first"
                );
              domConstruct.create('div',
                              {id: "patientSynopsisBottomContentPaneVisits"},
                            "patientSynopsisBottomContentPaneAdmissions",
                            "after"
              );
                domConstruct.create('div',
                                  {id: "patientNewVisitNotes"},
                                "patientSynopsisBottomContentPaneVisits",
                                "first"
                );

      /*
      domConstruct.create('div',
                          {id: "patientContactTab"},
                         "patientSummaryTab",
                         "after"
      );
        
        domConstruct.create('div',
                            {id: "contact_list"},
                            "patientContactTab",
                            "first"
        );
        domConstruct.create('div',
                            {id: "phone_list"},
                            "patientContactTab",
                            "last"
        );
        */

      domConstruct.create('div',
                          {id: "patientHistoryTab"},
                          "patientContextTabs",
                          "last"
      );

        domConstruct.create('div',
                            {id: "patientHistoryTabs"},
                            "patientHistoryTab",
                            "first"
        );
          domConstruct.create('div',
                              {id: "patientDemographicsTab"},
                              "patientHistoryTabs",
                              "first"
          );
            domConstruct.create('div',
                                {id: "demographics_add_or_edit_form"},
                                "patientDemographicsTab",
                                "first"
            );
            domConstruct.create('div',
                                {id: "guardian_list"},
                                "demographics_add_or_edit_form",
                                "after"
            );
          domConstruct.create('div',
                              {id: "patientSocialHistoryTab"},
                              "patientHistoryTabs",
                              "first"
          );
          domConstruct.create('div',
                              {id: "patientFamilyHistoryTab"},
                              "patientHistoryTabs",
                              "last"
          );
            domConstruct.create('div',
                                {id: "family_history_list"},
                                "patientFamilyHistoryTab",
                                "first"
            );
          domConstruct.create('div',
                              {id: "patientMedicalAndSurgicalHistoryTab"},
                              "patientHistoryTabs",
                              "last"
          );
/*
            domConstruct.create('div',
                                {id: "medical_and_surgical_history_list"},
                                "patientMedicalAndSurgicalHistoryTab",
                                "first"
            );
*/
            domConstruct.create('div',
                                {id: "medical_history_list"},
                                "patientMedicalAndSurgicalHistoryTab",
                                "first"
            );
            domConstruct.create('div',
                                {id: "surgical_history_list"},
                                "patientMedicalAndSurgicalHistoryTab",
                                "last"
             );

    domConstruct.create('div',
                          {id: "patientPreventiveHealthTab"},
                          "patientContextTabs",
                          "last"
      );
        domConstruct.create('div',
                            {id: "patientPreventiveTabs"},
                            "patientPreventiveHealthTab",
                            "first"
        );
          domConstruct.create('div',
                              {id: "patientNeonatalAndPaediatricExamTab"},
                              "patientPreventiveTabs",
                              "first"
          );
            domConstruct.create('div',
                                {id: "neonatal_and_paediatric_exam_list"},
                                "patientNeonatalAndPaediatricExamTab",
                                "first"
            );
          domConstruct.create('div',
                              {id: "patientImmunisationTab"},
                              "patientPreventiveTabs",
                              "last"
          );
            domConstruct.create('div',
                                {id: "immunisation_list"},
                                "patientImmunisationTab",
                                "first"
            );
          domConstruct.create('div',
                              {id: "patientObstetricsPreventivesTab"},
                              "patientPreventiveTabs",
                              "last"
          );

            domConstruct.create('div',
                                {id: "obstetric_history_detail"},
                                "patientObstetricsPreventivesTab",
                                "first"
            );
/*
            domConstruct.create('div',
                                {id: "obstetric_history_form"},
                                "obstetrics_history_detail",
                                "after"
            );
*/

          domConstruct.create('div',
                              {id: "patientGynaecologyPreventivesTab"},
                              "patientPreventiveTabs",
                              "last"
          );
            domConstruct.create('div',
                                {id: "gynaecology_preventives_list"},
                                "patientGynaecologyPreventivesTab",
                                "first"
            );
          
          domConstruct.create('div',
                              {id: "patientMedicalPreventivesTab"},
                              "patientPreventiveTabs",
                              "last"
          );
            domConstruct.create('div',
                                {id: "medical_preventives_list"},
                                "patientMedicalPreventivesTab",
                                "first"
            );
          
      /*
      domConstruct.create('div',
                          {id: "patientMedicationListAndAllergiesTab"},
                          "patientContextTabs",
                          "last"
      );
      */
      

      /*
      domConstruct.create('div',
                          {id: "patientAdmissionAndVisitsTab"},
                          "patientContextTabs",
                          "last"
      );
          domConstruct.create('div',
                              {id: "admission_list"},
                              "patientAdmissionAndVisitsTab",
                              "first"
          );
          domConstruct.create('div',
                              {id: "visit_list"},
                              "admission_list",
                              "after"
          );
      */
      /*
      domConstruct.create('div',
                          {id: "patientMediaTab"},
                          "patientContextTabs",
                          "last"
      );
          domConstruct.create('div',
                              {id: "patient_media_list"},
                              "patientMediaTab", "first"
          );
      */

      console.log("Created all the necessary DOM ELements.. Creating Dijits")

      var mainBorderContaner = registry.byId("patientTabsBorderContainer");
      domStyle.set(mainBorderContaner.domNode,
                        {"height":"50em","width":"100em","overflow":"auto"}
      );

        var sideBarContentPane = new ContentPane({id     : "patientSidebarContentPane",
                                                  region :"leading",
                                                  splitter:true,
                                                  style :"width:18em;"
                                              },
                                            "patientSidebarContentPane"
        );
        mainBorderContaner.addChild(sideBarContentPane);

          var sideBarTabContainer = new TabContainer({id     : "patientSidebarTabContainer",
                                                tabStrip  : true,
                                                tabPosition:'bottom',
                                                },
                                              "patientSidebarTabContainer"
          );
          sideBarContentPane.addChild(sideBarTabContainer)

            var sidebarTreeContainer = new ContentPane({id     : "patientTreeContainer",
                                                    title  : "Tree",
                                                    iconClass:"navigationIcon"
                                                  },
                                                "patientTreeContainer"
            );
            sideBarTabContainer.addChild(sidebarTreeContainer);
            var sidebarContactContainer = new ContentPane({id     : "patientSidebarDiv_contact",
                                                          title   : "Contact",
                                                          iconClass:"contactIcon"
                                                  },
                                                "patientSidebarDiv_contact"
            );
            sideBarTabContainer.addChild(sidebarContactContainer);
            var sidebarMediaContainer = new ContentPane({id     : "patientSidebarDiv_media",
                                                  title : "Media",
                                                  iconClass:"mediaIcon"
                                                  },
                                                "patientSidebarDiv_media"
            );
            sideBarTabContainer.addChild(sidebarMediaContainer);  

          console.log("Created patientTreeContainer Dijit")
          console.log("Adding patientTreeContainer Dijit to the BorderContainer")
          console.log("Added all the sidebar dijits..")

        var mainContainer = new ContentPane({id  : "patientContextContainer",
                                            region  : "center",
                                            splitter:true,
                                           },
                                           "patientContextContainer"
        );

        console.log("Created patientContextContainer Dijit")
        console.log("Adding patientContextContainer Dijit to the BorderContainer")

        mainBorderContaner.addChild(mainContainer);
        var tabs = new TabContainer({
                                      id: "patientContextTabs",
                                      tabPosition:"top",
                                      tabStrip:true,
                                      style : "min-height: 550px;overflow:auto;"
                                    },
                                    "patientContextTabs"
                                    );
        console.log("Created patientContextTabs Dijit")
        mainContainer.addChild(tabs);
        console.log("Added patientContextTabs to patientContextContainer Dijit");

        var summaryTab = new ContentPane({id:"patientSummaryTab",
                                          title:"Synopsis"
                                          },
                                          "patientSummaryTab"
                                          );
        tabs.addChild(summaryTab);
          var patientSynopsisBorderContainer = new BorderContainer({id:"patientSynopsisBorderContainer",
                                                                  //doLayout:true,
                                                                      },
                                            "patientSynopsisBorderContainer"
                                            );
          summaryTab.addChild(patientSynopsisBorderContainer);
            var patientSynopsisTopContentPane = new ContentPane({
                                                  id:"patientSynopsisTopContentPane",
                                                  region: "center",
                                                  splitter: true
                                                  },
                                              "patientSynopsisTopContentPane"
                                              );
            patientSynopsisBorderContainer.addChild(patientSynopsisTopContentPane);

            var patientSynopsisBottomContentPane = new ContentPane({
                                                          id:"patientSynopsisBottomContentPane",
                                                          region: "bottom",
                                                            splitter: true
                                                          },
                                            "patientSynopsisBottomContentPane"
                                            );
            patientSynopsisBorderContainer.addChild(patientSynopsisBottomContentPane);
              var patientSynopsisBottomTabContainer = new TabContainer({
                                                            id:"patientSynopsisBottomTabContainer",
                                                            tabStrip:true,
                                                            tabPosition:"top",
                                                            nested: true
                                                            },
                                              "patientSynopsisBottomTabContainer"
                                              );
              patientSynopsisBottomContentPane.addChild(patientSynopsisBottomTabContainer);
                var patientSynopsisBottomContentPaneAdmissions = new ContentPane({
                                                            id:"patientSynopsisBottomContentPaneAdmissions",
                                                            title : "Admissions",
                                                            },
                                              "patientSynopsisBottomContentPaneAdmissions"
                                              );
                patientSynopsisBottomTabContainer.addChild(patientSynopsisBottomContentPaneAdmissions);
                  var admissionNotesEditor = new Editor({id:"patientNewAdmissionNotes"},"patientNewAdmissionNotes");
                  patientSynopsisBottomContentPaneAdmissions.addChild(admissionNotesEditor);
                var patientSynopsisBottomContentPaneVisits = new ContentPane({
                                                            id:"patientSynopsisBottomContentPaneVisits",
                                                            title: "Visits",
                                                            },
                                              "patientSynopsisBottomContentPaneVisits"
                                              );
                patientSynopsisBottomTabContainer.addChild(patientSynopsisBottomContentPaneVisits);
                  var visitNotesEditor = new Editor({id:"patientNewVisitNotes"},"patientNewVisitNotes");
                  patientSynopsisBottomContentPaneVisits.addChild(visitNotesEditor);

  /*
        var contactTab = new ContentPane({id:"patientContactTab",
                                          title:"Contact"
                                          },
                                          "patientContactTab"
                                          );
        tabs.addChild(contactTab);
        */
        var historyTab = new ContentPane({id:"patientHistoryTab",
                                          title:"History"
                                          },
                                          "patientHistoryTab"
                                          );
        tabs.addChild(historyTab);
          var historyTabs = new TabContainer({id:"patientHistoryTabs",
                                              tabPosition:"top",
                                              tabStrip:true,
                                              nested : true,
                                              style : "min-height: 550px;overflow:auto;"
                                            },
                                            "patientHistoryTabs"
                                            );
          historyTab.addChild(historyTabs);
            var demographicsTab = new ContentPane({id:"patientDemographicsTab",
                                              title:"Demographics"
                                              },
                                              "patientDemographicsTab"
                                              );
            historyTabs.addChild(demographicsTab);
              var demographicsAddOrEditForm = new ContentPane({id:"demographics_add_or_edit_form"
                                                },
                                                "demographics_add_or_edit_form"
                                                );
              demographicsTab.addChild(demographicsAddOrEditForm);
            var socialHistoryTab = new ContentPane({id:"patientSocialHistoryTab",
                                              title:"Social"
                                              },
                                              "patientSocialHistoryTab"
                                              );
            historyTabs.addChild(socialHistoryTab);
            var familyHistoryTab = new ContentPane({id:"patientFamilyHistoryTab",
                                              title:"Family"
                                              },
                                              "patientFamilyHistoryTab"
                                              );
            historyTabs.addChild(familyHistoryTab);
            var medicalAndSurgicalHistoryTab = new ContentPane({id:"patientMedicalAndSurgicalHistoryTab",
                                              title:"Medical & Surgical"
                                              },
                                              "patientMedicalAndSurgicalHistoryTab"
                                              );
            historyTabs.addChild(medicalAndSurgicalHistoryTab);
  /*
              var medicalHistoryTab = new ContentPane({id:"medical_history_list"
                                                      },
                                                      "medical_history_list"
                                                      );
              medicalAndSurgicalHistoryTab.addChild(medicalHistoryTab);

              var surgicalHistoryTab = new ContentPane({id:"surgical_history_list"
                                                      },
                                                      "surgical_history_list"
                                                      );
              medicalAndSurgicalHistoryTab.addChild(surgicalHistoryTab);
  */

        var preventiveHealthTab = new ContentPane({id:"patientPreventiveHealthTab",
                                                  title:"Preventives"
                                                  },
                                                  "patientPreventiveHealthTab"
                                                  );
        tabs.addChild(preventiveHealthTab);
          var preventiveHealthTabs = new TabContainer({id:"patientPreventivesTabs",
                                                        tabPosition:"top",
                                                        tabStrip:true,
                                                        nested : true,
                                                        style : "min-height: 550px;overflow:auto;"
                                                    },
                                                    "patientPreventiveTabs"
                                                    );
          preventiveHealthTab.addChild(preventiveHealthTabs);

            var patientImmunisationTab = new ContentPane({id:"patientImmunisationTab",
                                                      title:"Immunisation"
                                                      },
                                                      "patientImmunisationTab"
                                                      );
            preventiveHealthTabs.addChild(patientImmunisationTab);

            var patientObstetricsPreventivesTab = new ContentPane({id:"patientObstetricsPreventivesTab",
                                                        title:"Obstetrics"
                                                        },
                                                        "patientObstetricsPreventivesTab"
                                                        );
            preventiveHealthTabs.addChild(patientObstetricsPreventivesTab);


              var patientObstetricsHistoryDetail = new ContentPane({id:"obstetric_history_detail",
                                                          },
                                                          "obstetric_history_detail"
                                                          );
              patientObstetricsPreventivesTab.addChild(patientObstetricsHistoryDetail);
  /*
              var patientObstetricsHistoryForm = new ContentPane({id:"obstetric_history_form",
                                                          },
                                                          "obstetric_history_form"
                                                          );
              patientObstetricsPreventivesTab.addChild(patientObstetricsHistoryForm);
  */

            var patientGynaecologyPreventivesTab = new ContentPane({id:"patientGynaecologyPreventivesTab",
                                                        title:"Gynaecology"
                                                        },
                                                        "patientGynaecologyPreventivesTab"
                                                        );
            preventiveHealthTabs.addChild(patientGynaecologyPreventivesTab);

            var patientMedicalPreventivesTab      = new ContentPane({id:"patientMedicalPreventivesTab",
                                                        title:"Medical & Surgical",
                                                        disabled: true
                                                        },
                                                        "patientMedicalPreventivesTab"
                                                        );
            preventiveHealthTabs.addChild(patientMedicalPreventivesTab);

            var patientNeonatalAndPaediatricTab = new ContentPane({id:"patientNeonatalAndPaediatricExamTab",
                                                        title:"Neonatal & Paediatric",
                                                        disabled: true
                                                        },
                                                        "patientNeonatalAndPaediatricExamTab"
                                                        );
            preventiveHealthTabs.addChild(patientNeonatalAndPaediatricTab);
        /*
        var medicationAndAllergiesTab = new ContentPane({id:"patientMedicationListAndAllergiesTab",
                                                        title:"Medications & Allergies"
                                                        },
                                                        "patientMedicationListAndAllergiesTab"
                                                        );
        tabs.addChild(medicationAndAllergiesTab);
        */
        /*
        var admissionAndVisitTab      = new ContentPane({id:"patientAdmissionAndVisitsTab",
                                                        title:"Admissions & Visits"
                                                        },
                                                        "patientAdmissionAndVisitsTab"
                                                        );
        tabs.addChild(admissionAndVisitTab);
        */
        /*
        var mediaTab                 = new ContentPane({id:"patientMediaTab",
                                                        title:"Media"
                                                        },
                                                        "patientMediaTab"
                                                        );
        tabs.addChild(mediaTab);
        */

      mainContainer.startup();
     //tabs.startup();
     //historyTabs.startup();
     //preventiveHealthTabs.startup();

     console.log("Building Patient Tree..")
     buildPatientTree();
     console.log("Finished Building Patient Tree..")

     mainBorderContaner.resize();
     patientSynopsisBorderContainer.resize();
     //registry.byId("patientTabsBorderContainer").resize();
     registry.byId("centerMainPane").resize();

     //domStyle.set("patientContactTab",{'display':"none"});


//{% if perms.patient.add_patientcontact %}
     /*{% comment %}
    var addContactButton =  new Button({
                                  label: "Add",
                                  title: "Add New Contact Details",
                                  iconClass: "addPatientContactIcon_16",
                                  onClick: function(){
                                            require(["dojo/_base/xhr", "dojo/_base/array"],
                                            function(xhr, array){
                                                xhr.get({
                                                        url: "{%url contact_json %}"+
                                                             "?patient_id="+
                                                             dom.byId("selected_patient_id_info").innerHTML +
                                                             "&action=add",
                                                        load: function(html){
                                                                      var myDialog = dijit.byId("editPatientDialog");
                                                                      myDialog.set('content', html);
                                                                      myDialog.set('title', "Add Postal Address Information");
                                                                      myDialog.show();
                                                              }
                                                 });
                                            });
                                 }
                              },
                              domConstruct.create('button',
                                                  {type : "button",
                                                   id   : "addContactButton"
                                                  },
                                                  "contact_list",
                                                  "before"
                              )
    );
*/
//{% endif %}


//{% if perms.patient.add_patientphone %}
/*
    var addPhoneButton =  new Button({
                                    label: "Add",
                                    title: "Add New Phone Numbers",
                                    iconClass: "addPatientPhoneIcon_16",
                                    onClick: function(){
                                           require(
                                            ["dojo/_base/xhr", "dojo/_base/array"],
                                            function(xhr, array){
                                              xhr.get({
                                                url: "{%url phone_json %}"+"?patient_id="+
                                                       dom.byId("selected_patient_id_info").innerHTML +
                                                      "&action=add",
                                                load: function(html){
                                                             var myDialog = dijit.byId("editPatientDialog");
                                                             myDialog.set('content', html);
                                                             myDialog.set('title', "Add Phone Numbers");
                                                             myDialog.show();
                                                       }
                                             });
                                           })
                                    }
                         },
                         domConstruct.create('button',
                                            {type :"button",
                                             id   :"addPhoneButton"
                                            },
                                            "phone_list",
                                            "before"
                         )
  );
 {% endcomment %}*/
//{% endif %}

//{%if perms.patient.add_patientguardian %}
    var addGuardianButton =  new Button({
                                        label: "Add",
                                        title:"Add Guardian Details",
                                        iconClass: "dijitIconNewTask",
                                        onClick: function(){
                                               require(
                                                ["dojo/_base/xhr", "dojo/_base/array"],
                                                function(xhr, array){
                                                  xhr.get({
                                                    url: "{%url guardian_json %}"+"?patient_id="+
                                                          dom.byId("selected_patient_id_info").innerHTML +
                                                          "&action=add",
                                                    load: function(html){
                                                             var myDialog = dijit.byId("editPatientDialog");
                                                             myDialog.set('content', html);
                                                             myDialog.set('title', "Add Guardian Information ");
                                                             myDialog.show();
                                                          }
                                                 });
                                               })
                                        }
                         },
                         domConstruct.create('button',
                                              {type : "button",
                                               id   : "addGuardianButton"
                                              },
                                              "guardian_list",
                                              "before")
    );
//{% endif %}

    /*
//{% if perms.admission.add_admissiondetail %}
     {% comment %}
    var addAdmissionButton =  new Button({
                                        label: "Add",
                                        title:"Add New Admission",
                                        iconClass: "dijitIconNewTask",
                                        onClick: function(){
                                               require(
                                                ["dojo/_base/xhr", "dojo/_base/array"],
                                                function(xhr, array){
                                                  //var gridRow    = grid.selection.getSelected();
                                                  //var id = grid.store.getValue(gridRow[0], 'id');
                                                  xhr.get({
                                                    url: "{%url admission_json %}"+
                                                          "?patient_id="+
                                                          dom.byId("selected_patient_id_info").innerHTML +
                                                          "&action=add",
                                                    load: function(html){
                                                               var myDialog = dijit.byId("editPatientDialog");
                                                               myDialog.set('content', html);
                                                               myDialog.set('title',
                                                                            "Record New Admission to the Clinic ");
                                                               myDialog.show();
                                                          }
                                                 });
                                               })
                                        }
                                      },
                                      domConstruct.create('button',
                                                          {type : "button",
                                                           id   : "addAdmissionButton"
                                                          },
                                                          "admission_list",
                                                          "before"
                                      )
);
//{% endif %}

//{% if perms.visit.add_visitdetail %}
    var addVisitButton =  new Button({
                                    label: "Add",
                                    title: "Add New OPD Visit",
                                    iconClass: "dijitIconNewTask",
                                    onClick: function(){
                                           require(
                                            ["dojo/_base/xhr", "dojo/_base/array"],
                                            function(xhr, array){
                                              xhr.get({
                                                url: "{%url visit_json %}"+
                                                     "?patient_id="+
                                                     dom.byId("selected_patient_id_info").innerHTML +
                                                     "&action=add",
                                                load: function(html){
                                                           var myDialog = dijit.byId("editPatientDialog");
                                                           myDialog.set('content', html);
                                                           myDialog.set('title', " Record New Out Patient Visit ");
                                                           myDialog.show();
                                                      }
                                             });
                                           })
                                    }
                         },
                         domConstruct.create('button',
                                              {type : "button",
                                               id   : "addVisitButton"
                                              },
                                              "visit_list",
                                              "before"
                         )
  );
{% endcomment %}
//{% endif %}
*/

//{% comment %}
//{% if perms.patient %}
    var addDemographicsButton =  new Button({
                                          label: "Add",
                                          title: "Add Demographics Data",
                                          iconClass: "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url demographics_json %}"+
                                                           "?patient_id=" +
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record Demographics Information");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                         },
                          domConstruct.create('button',
                                              {type : "button",
                                               id   : "addDemographicsButton"
                                              },
                                              "demographics_add_or_edit_form",
                                              "before"
                          )
);
//{% endif %}
//{%endcomment%}

//{% if perms.patient %}
    var addAllergyButton =  new Button({
                                      label: "Add",
                                      title: "Add Allergy Details",
                                      iconClass: "dijitIconNewTask",
                                      style    :"position:relative; top: 0; left: 0;",
                                      onClick: function(){
                                             require(
                                              ["dojo/_base/xhr", "dojo/_base/array"],
                                              function(xhr, array){
                                                xhr.get({
                                                  url: "{% url allergies_json %}"+
                                                       "?patient_id="+
                                                       dom.byId("selected_patient_id_info").innerHTML +
                                                       "&action=add",
                                                  load: function(html){
                                                             var myDialog = dijit.byId("editPatientDialog");
                                                             myDialog.set('content', html);
                                                             myDialog.set('title', "Record New Allergy Details");
                                                             myDialog.show();
                                                        }
                                               });
                                             })
                                      }
                         },
                        domConstruct.create('button',
                                            {type : "button",
                                             id   : "addAllergyButton"
                                            },
                                            "allergy_list",
                                            "before"
                        )
);
//{% endif %}

//{% if perms.patient %}
    var addPatientImmunisationButton =  new Button({
                                          label: "Add",
                                          title: "Add Immunisation Details",
                                          iconClass: "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url immunisation_json %}"+
                                                           "?patient_id="+
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record New Immunisation Details");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                                       },
                                      domConstruct.create('button',
                                                          {type : "button",
                                                           id   : "addPatientImmunisationButton"
                                                          },
                                                          "immunisation_list",
                                                          "before"
                                      )
);
//{% endif %}

//{% if perms.patient %}
    var addPatientFamilyHistoryButton =  new Button({
                                          label       : "Add",
                                          title       : "Add Family History Details",
                                          iconClass   : "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url family_history_json %}"+
                                                           "?patient_id="+
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record New Family History Details");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                         },
                         domConstruct.create('button',
                                            {type : "button",
                                             id   : "addPatientFamilyHistoryButton"
                                            },
                                            "family_history_list",
                                            "before"
                         )
);


//{% endif %}

//{% if perms.patient %}
    var addPatientMedicalHistoryButton =  new Button({
                                          label       : "Add",
                                          title       : "Add Medical History Details",
                                          iconClass   : "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url medical_history_json %}"+
                                                           "?patient_id="+
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record New Medical History Details");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                         },
                         domConstruct.create('button',
                                            {type : "button",
                                             id   : "addPatientMedicalHistoryButton"
                                            },
                                            "medical_history_list",
                                            "before"
                         )
);


//{% endif %}

//{% if perms.patient %}
    var addPatientSurgicalHistoryButton =  new Button({
                                          label       : "Add",
                                          title       : "Add Surgical History Details",
                                          iconClass   : "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url surgical_history_json %}"+
                                                           "?patient_id="+
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record New Surgical History Details");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                         },
                         domConstruct.create('button',
                                            {type : "button",
                                             id   : "addPatientSurgicalHistoryButton"
                                            },
                                            "surgical_history_list",
                                            "before"
                         )
);

//{% endif %}


//{% if perms.patient %}
    var addPatientMedicationListButton =  new Button({
                                          label: "Add",
                                          title : "Add New Medication List",
                                          iconClass: "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url medication_list_json%}"+
                                                           "?patient_id="+
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record Medication Details");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                         },
                        domConstruct.create('button',
                                            {type : "button",
                                             id   : "addPatientMedicationListButton"
                                            },
                                            "medication_list",
                                            "before"
                        )
);
//{% endif %}

//{% comment %}
//{% if perms.patient %}
    var addPatientMediaButton =  new Button({
                                          label: "Add",
                                          title : "Add Patient Media Attachements",
                                          iconClass: "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "/AuShadha/pat/media/"+
                                                           "?patient_id="+
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Add Patient Media");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                                  },
                                  domConstruct.create('button',
                                                      {type : "button",
                                                       id   : "addPatientMediaButton"
                                                      },
                                                      "patientMediaTab",
                                                      "first"
                                  )
);
//{% endif %}
//{% endcomment %}
    }

   });
  });

}

//patientContextTabSetup();
