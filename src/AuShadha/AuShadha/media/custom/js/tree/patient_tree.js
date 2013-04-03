function buildPatientTree(){
  require([
      "dojo/_base/window",

      "dojo/store/Memory",
      "dijit/tree/ObjectStoreModel",
      "dijit/Tree",
      "dijit/tree/ForestStoreModel",
      "dojo/data/ItemFileReadStore",

      "dojo/dom",
      "dijit/registry",
      "dojo/dom-construct",
      "dojo/dom-style",
      "dojo/json"
  ], 
  function(win,
          Memory, 
          ObjectStoreModel,
          Tree,
          ForestStoreModel,
          ItemFileReadStore,
          dom, 
          registry,
          domConstruct, 
          domStyle, 
          JSON){

    // Create store 
    var patientTreeStore = new ItemFileReadStore({url: CHOSEN_PATIENT.patientTreeUrl,
                                                  clearOnClose:true,
                                                  heirarchial:false
    });
    console.log("Patient Tree Store is: ");
    console.log(patientTreeStore);

    // Create the model
    var patientTreeModel = new ForestStoreModel({store         : patientTreeStore,
                                                 query         : {type: 'application'},
                                                 rootId        : 'root',
                                                 rootLabel     : "Patient",
                                                 childrenAttrs : ["children"]
                                                });

    // Create the Tree.
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

    console.log("Trying to build the Patient Tree");

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
                                ){
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
                                  }
                                );

                                query('#patientSynopsisContainer > div :hover').
                                  forEach( function(node, index, nodeList){
                                    console.log("setting styles...")
                                    domStyle.set(node,
                                                {
                                                  background   : "#faf9ff",
                                                }
                                    );
                                  }
                                );

                              },
                              function(error){
                                  publishError("ERROR!: " + error);
                              }
                            );
                          }
                        )
                      }

                      if (item.name == "Medical History" || 
                          item.type == 'medical_history_module'){
//                             setUpVisitTab();
//                               createHistoryTabs();
                      }

                      if (item.name == "Surgical History" || 
                          item.type == 'surgical_history_module'){
//                             setUpVisitTab();
                      }

                      if (item.name == "Demographics" || 
                          item.type == 'demographics_module'){

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
          }
        },
        'patientTreeDiv');

        patientTree.getIconClass = setTreeIcons;
        console.log("Setting Tree icons complete");
        patientTree.startup();
        patientTree.expandAll();
        //patientTree.collapseAll();
    });
}