function buildPatientTree(){
  require([
      "dojo/ready",
      "dojo/_base/window",

      "dojo/store/Memory",
      "dijit/tree/ObjectStoreModel",
      "dijit/Tree",
      "dijit/tree/ForestStoreModel",
      "dojo/data/ItemFileReadStore",

      "dojo/dom",
      "dijit/registry",
      "dojo/dom-construct","dojo/dom-style","dojo/json"
  ], function(ready, win,
              Memory, ObjectStoreModel,
              Tree,
              ForestStoreModel,
              ItemFileReadStore,
              dom, registry,
              domConstruct, domStyle, JSON){

    var existingTree = registry.byId('patientTreeDiv');

     if(existingTree){
       console.log("Tree exists.. proceeding to destroy it..")
       existingTree.destroyRecursive();
     }

     console.log(registry.byId("patientTreeDiv"));
     if(!dom.byId("patientTreeDiv")){
        domConstruct.create('div',
                            {id: "patientTreeDiv"},
                            "patientTreeContainer",
                            "first"
        );
        domStyle.set( dom.byId('patientTreeDiv'),{'minWidth':'200px',
                                                  'maxWidth':'300px',
                                                  'minHeight':"400px",
                                                  'overflow':"auto"
        });
    }  

     // Create store 
     var patientTreeStore = new ItemFileReadStore({url: CHOSEN_PATIENT.patientTreeUrl,
                                                   clearOnClose:true,
                                                  heirarchial:false
    });
    console.log(patientTreeStore);
     // Create the model
      var patientTreeModel = new ForestStoreModel({
          store: patientTreeStore,
          query: {type: 'application'},
          rootId: 'root',
          rootLabel:"Patient",
          childrenAttrs:["children"]
      });
     
     /*
      var patientTreeStore = new Memory({
          data: [
              { id: 'patient',
                name:'Patient',
                type:'trunk'
              },
/*
                { id: 'contact',
                  name:'Contact',
                  type:'main_branch',
                  parent: 'patient'
                },
                    { id: 'address',
                      name:'Address',
                      type:'second_branch',
                      parent: 'contact'
                    },
                    { id: 'phone',
                      name:'Phone',
                      type:'second_branch',
                      parent: 'contact'
                    },
*/
/*
                { id: 'history',
                  name:'History',
                  type:'main_branch',
                  parent: 'patient'
                },
                    { id: 'demographics',
                      name:'Demographics',
                      type:'second_branch',
                      parent: 'history'
                    },
                    { id: 'social',
                      name:'Social',
                      type:'second_branch',
                      parent: 'history'
                    },
                    { id: 'family',
                      name:'Family',
                      type:'second_branch',
                      parent: 'history'
                    },

                    { id: 'medical_history',
                      name:'Medical',
                      type:'second_branch',
                      parent: 'history'
                    },
                    { id: 'surgical_history',
                      name:'Surgical',
                      type:'second_branch',
                      parent: 'history'
                    },

                { id: 'preventives',
                  name:'Preventives',
                  type:'main_branch',
                  parent: 'patient'
                },
                    { id: 'neonatal_and_paediatric_preventives',
                      name:'Neonatal & Paediatric',
                      type:'second_branch',
                      parent: 'preventives'
                    },
                    { id: 'immunisation',
                      name:'Immunisation',
                      type:'second_branch',
                      parent: 'preventives'
                    },
                    { id: 'obstetric_preventives',
                      name:'Obstetrics',
                      type:'second_branch',
                      parent: 'preventives'
                    },
                    { id: 'gynaecology_preventives',
                      name:'Gynaecology',
                      type:'second_branch',
                      parent: 'preventives'
                    },
                    { id: 'medical_and_surgical_preventives',
                      name:'Medical & Surgical',
                      type:'second_branch',
                      parent: 'preventives'
                    },

                { id: 'medication_and_allergies',
                  name:'Medications & Allergies',
                  type:'main_branch',
                  parent: 'patient'
                },

                    { id: 'medication_list',
                      name:'Medications',
                      type:'second_branch',
                      parent: 'medication_and_allergies'
                    },
                    { id: 'allergy_list',
                      name:'Allergies',
                      type:'second_branch',
                      parent: 'medication_and_allergies'
                    },
*/
/*
                { id: 'visits',
                  name:'Visits',
                  type:'main_branch',
                  parent: 'patient'
                },
                { id: 'admissions',
                  name:'Admissions',
                  type:'main_branch',
                  parent: 'patient'
                },
                { id: 'investigations',
                  name:'Investigations',
                  type:'main_branch',
                  parent: 'patient'
                },
                { id: 'imaging',
                  name:'Imaging',
                  type:'main_branch',
                  parent: 'patient'
                },
*/
/*
                { id: 'patient_media',
                  name:'Media',
                  type:'main_branch',
                  parent: 'patient'
                },

                    { id: 'patient_documents',
                      name:'Documents',
                      type:'second_branch',
                      parent: 'patient_media'
                    },
                    { id: 'patient_images',
                      name:'Images',
                      type:'second_branch',
                      parent: 'patient_media'
                    },
                    { id: 'patient_videos',
                      name:'Videos',
                      type:'second_branch',
                      parent: s'patient_media'
                    }
*/
/*
          ],
          getChildren: function(object){
              return this.query({parent: object.id});
          }

      });

      // Create the model
      var patientTreeModel = new ObjectStoreModel({
          store: patientTreeStore,
          query: {id: 'patient'},
          labelAttr: "name"
      });
  */


      // Create the Tree.
      ready(function(){

          function setTreeIcons(item, opened){
            //console.log(item.tree.rootNode || "Not defined");
            if(item.id=='root'){
              console.log(item.id)
              console.log("Returning iconclass for tree root..")
              return 'patientIcon'
            }
            else{
              console.log(item.id)
              console.log("Returning iconclass for tree root..")
              return (opened ? "dijitFolderOpened" : "dijitFolderClosed")
            }
          }

          var demographicsUrlDict = {demographicsUrl   : CHOSEN_PATIENT.demographicsadd,
                                     contactUrl        : CHOSEN_PATIENT.contactjson,
                                     phoneUrl          : CHOSEN_PATIENT.phonejson,
                                     guardianUrl       : CHOSEN_PATIENT.guardianjson
                                    }

          var patientTree = new Tree({
              model   : patientTreeModel,
              showRoot: false,
              onClick : function(item){

                          var allowed_items     = ['Visits','Admissions',"Investigations","Imaging"];
                          var centerTopTabPane  = registry.byId("centerTopTabPane");

                          if (item.name == "Synopsis" || item.id == 'SYNOPSIS'){
                            require(['dojo/dom',
                                    'dijit/registry',
                                    'dojo/dom-style',
                                    'dojo/query',
                                    'dojo/dom-construct',
                                    'dijit/form/Button',
                                    'dijit/Dialog',
                                    'dijit/layout/BorderContainer',
                                    'dojox/layout/ContentPane',
                                    'dijit/layout/TabContainer',
                                    'dojo/json','dojo/request'
                                    ],
                            function(dom,registry,
                                     domStyle,query,
                                     domConstruct,
                                     Button, 
                                     Dialog,
                                     BorderContainer,
                                     ContentPane,
                                     TabContainer, 
                                     JSON,
                                     request
                                    )
                              {
                                request(CHOSEN_PATIENT.patientsummary).
                                then(
                                  function(html){
                                    
                                    if(dom.byId('patientSynopsisContainer')){
                                      dom.byId('patientSynopsisContainer').remove();
                                    }
                                    domConstruct.create('div',
                                                        {id: 'patientSynopsisContainer'},
                                                        'patientSynopsisTopContentPane',
                                                        'first');
                                    dom.byId('patientSynopsisContainer').innerHTML = html;

//                                     domConstruct.create('div',
//                                                         {id: 'patientHistoryContainer'},
//                                                         'patientSynopsisContainer',
//                                                         0);
//                                       domConstruct.create('div',
//                                                           {id: 'patientMedicalHistoryContainer'},
//                                                           'patientHistoryContainer',
//                                                           0);
//                                       domConstruct.create('div',
//                                                           {id: 'patientSurgicalHistoryContainer'},
//                                                           'patientHistoryContainer',
//                                                           1);
//                                       domConstruct.create('div',
//                                                           {id: 'patientFamilyHistoryContainer'},
//                                                           'patientHistoryContainer',
//                                                           2);
//                                       domConstruct.create('div',
//                                                           {id: 'patientSocialHistoryContainer'},
//                                                           'patientHistoryContainer',
//                                                           3);
//                                       domConstruct.create('div',
//                                                           {id: 'patientDemographicsContainer'},
//                                                           'patientHistoryContainer',
//                                                           4);
// 
//                                     domConstruct.create('div',
//                                                         {id: 'patientPreventivesContainer'},
//                                                         'patientSynopsisContainer',
//                                                         2);
//                                       domConstruct.create('div',
//                                                             {id: 'patientImmunisationContainer'},
//                                                             'patientPreventivesContainer',
//                                                             0);
//                                       domConstruct.create('div',
//                                                             {id: 'patientObstetricHistoryDetailContainer'},
//                                                             'patientPreventivesContainer',
//                                                             1);
//                                       domConstruct.create('div',
//                                                             {id: 'patientMedicalPreventivesContainer'},
//                                                             'patientPreventivesContainer',
//                                                             2);
// 
//                                     domConstruct.create('div',
//                                                         {id: 'patientMedicationListContainer'},
//                                                         'patientSynopsisContainer',
//                                                         3);
//                                     domConstruct.create('div',
//                                                         {id: 'patientAllergyContainer'},
//                                                         'patientSynopsisContainer',
//                                                         4);
//                                     domConstruct.create('div',
//                                                         {id: 'patientInvContainer'},
//                                                         'patientSynopsisContainer',
//                                                         5);
//                                     domConstruct.create('div',
//                                                         {id: 'patientImagingContainer'},
//                                                         'patientSynopsisContainer',
//                                                         6);
//                                     domConstruct.create('div',
//                                                         {id: 'patientDiagnosisContainer'},
//                                                         'patientSynopsisContainer',
//                                                         7);
//                                     domConstruct.create('div',
//                                                         {id: 'patientProceduresContainer'},
//                                                         'patientSynopsisContainer',
//                                                         8);
                                      query('#patientSynopsisContainer > div').
                                      forEach( function(node, index, nodeList){
                                        console.log("setting styles...")
                                        domStyle.set(node,
                                                     {borderRadius : "2px",
                                                      background   : "white",
                                                      border       : "solid #ddd 1px",
                                                      minHeight    : " 10em",
                                                      margin       : "3px",
                                                      padding      : "10px"
                                                     }
                                        );
                                      });
                                      query('#patientSynopsisContainer > div :hover').
                                      forEach( function(node, index, nodeList){
                                        console.log("setting styles...")
                                        domStyle.set(node,
                                                     {
                                                      background   : "#faf9ff",
                                                     }
                                        );
                                      });
                                  },
                                  function(error){
                                      publishError("ERROR!: " + error);
                                  }
                                )
                              }
                            )
                          }

                          if (item.name == "Medical History" || item.type == 'medical_history_module'){
//                             setUpVisitTab();
//                               createHistoryTabs();
                          }

                          if (item.name == "Surgical History" || item.type == 'surgical_history_module'){
//                             setUpVisitTab();
                          }

                          if (item.name == "Demographics" || item.type == 'demographics_module'){
                          }

              },
              onDblClick: function(item,node,evt){
                            var contextTabs = registry.byId('patientContextTabs');
                            if(item.name =="Demographics" || item.type=="demographics_module"){
                                    if(!registry.byId('contactAndDemographicsTab') ){
                                        console.log(CHOSEN_PATIENT);
                                        makeDemographicsTab(demographicsUrlDict);
                                    }
                                    else{
                                      registry.byId("patientContextTabs").selectChild(
                                        registry.byId("contactAndDemographicsTab")
                                      );
                                    }
                            }
                            if(item.name =="Social History" || item.type=="social_history_module"){
                                    if(!registry.byId('socialHistoryTab') ){
                                        console.log(CHOSEN_PATIENT);
                                        makeSocialHistoryTab(CHOSEN_PATIENT.socialhistoryadd);
                                    }
                                    else{
                                      registry.byId("patientContextTabs").selectChild(
                                        registry.byId("socialHistoryTab")
                                      );
                                    }
                            }
                            
                            if(item.name =="Family History" || item.type=="family_history_module"){
                                    if(!registry.byId('familyHistoryTab') ){
                                        console.log(CHOSEN_PATIENT);
                                        makeFamilyHistoryTab(CHOSEN_PATIENT.familyhistoryjson);
                                    }
                                    else{
                                      registry.byId("patientContextTabs").selectChild(
                                        registry.byId("familyHistoryTab")
                                      );
                                    }
                            }
                            
                            if(item.name =="Medical History" || item.type=="medical_history_module"){
                                    if(!registry.byId('patientMedicalHistoryTab') ){
                                        console.log(CHOSEN_PATIENT);
                                        makeMedicalHistoryTab(CHOSEN_PATIENT.medicalhistoryjson);
                                    }
                                    else{
                                      registry.byId("patientContextTabs").selectChild(
                                        registry.byId("patientMedicalHistoryTab")
                                      );
                                    }
                            }
                            
                            if(item.name =="Surgical History" || item.type=="surgical_history_module"){
                                    if(!registry.byId('patientSurgicalHistoryTab') ){
                                        console.log(CHOSEN_PATIENT);
                                        makeSurgicalHistoryTab(CHOSEN_PATIENT.surgicalhistoryjson);
                                    }
                                    else{
                                      registry.byId("patientContextTabs").selectChild(
                                        registry.byId("patientSurgicalHistoryTab")
                                      );
                                    }
                            }
                            if(item.name =="Medications" || item.type=="medication_list_module"){
                                    if(!registry.byId('medicationListTab') ){
                                        console.log(CHOSEN_PATIENT);
                                        makeMedicationListTab(CHOSEN_PATIENT.medicationlistjson);
                                    }
                                    else{
                                      registry.byId("patientContextTabs").selectChild(
                                        registry.byId("medicationListTab")
                                      );
                                    }
                            }
                            

//                             if(item.type == "family_history_module"   ||
//                                item.type == "medical_history_module"  || 
//                                item.type == "surgical_history_module" || 
//                                item.type == "social_history_module"
//                             ){
//                               //createHistoryTabs();
//                             }

                            if(item.type == "medical_history_module"){
                              createMedicalHistoryTab();
                            }

              }
           },
          'patientTreeDiv');

          patientTree.getIconClass = setTreeIcons;
          console.log("Setting Tree icons complete");

         //patientTree.placeAt('patientTreeDiv')
          patientTree.startup();
         //patientTree.expandAll();
         //patientTree.collapseAll();
      });

  });
}