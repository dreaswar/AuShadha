function buildVisitTree(){
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

    var existingTree = registry.byId('patientVisitTreeDiv');

     if(existingTree){
       console.log("Tree exists.. proceeding to destroy it..")
       existingTree.destroyRecursive();
     }

     console.log(registry.byId("patientVisitTreeDiv"));
     if(!dom.byId("patientVisitTreeDiv")){
        domConstruct.create('div',
                            {id: "patientVisitTreeDiv"},
                            "patientVisitTreeContainer",
                            "first"
        );
        domStyle.set( dom.byId('patientVisitTreeDiv'),{'minWidth':'200px',
                                                  'maxWidth':'300px',
                                                  'minHeight':"400px",
                                                  'overflow':"auto"
        });
    }

     // Create store
     var patientVisitTreeStore = new ItemFileReadStore({url: CHOSEN_PATIENT.visittree,
                                                        clearOnClose:true,
                                                        heirarchial:false
    });
    console.log(patientVisitTreeStore);


    // Create the model
      var patientVisitTreeModel = new ForestStoreModel({
          store: patientVisitTreeStore,
          query: {type: 'application'},
          rootId: 'root',
          rootLabel:"OPD Visits",
          childrenAttrs:["children"]
      });

//       var patientVisitTreeStore = new Memory({
//           data: [
//               { id: 'visit',
//                 name:'Visit 2013-02-01',
//                 type:'trunk'
//               },
//                 { id: 'synopsis',
//                   name:'Synopsis',
//                   type:'main_branch',
//                   parent: 'visit'
//                 },
//                 { id: 'investigations',
//                   name:'Investigations',
//                   type:'main_branch',
//                   parent: 'visit'
//                 },
//                 { id: 'imaging',
//                   name:'Imaging',
//                   type:'main_branch',
//                   parent: 'visit'
//                 },
// 
//                 { id: 'patient_media',
//                   name:'Media',
//                   type:'main_branch',
//                   parent: 'visit'
//                 },
// 
//                     { id: 'patient_documents',
//                       name:'Documents',
//                       type:'second_branch',
//                       parent: 'patient_media'
//                     },
//                     { id: 'patient_images',
//                       name:'Images',
//                       type:'second_branch',
//                       parent: 'patient_media'
//                     },
//                     { id: 'patient_videos',
//                       name:'Videos',
//                       type:'second_branch',
//                       parent: 'patient_media'
//                     }
// 
// 
//           ],
//           getChildren: function(object){
//               return this.query({parent: object.id});
//           }
// 
//       });

      // Create the model
//       var patientVisitTreeModel = new ObjectStoreModel({
//           store: patientVisitTreeStore,
//           query: {id: 'visit'},
//           labelAttr: "name"
//       });


      // Create the Tree.
      ready(function(){

          function setVisitTreeIcons(item, opened){
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

          var patientVisitTree = new Tree({
              model   : patientVisitTreeModel,
              showRoot: false,
              onClick: function(item){

												if (item.id == "NEW_OPD_VISIT"){
													var addVisitUrl = CHOSEN_PATIENT.visitadd;
													if( registry.byId("newVisitAddForm") != undefined){
														registry.byId("newVisitAddForm").destroyRecursive();
													}
													registry.byId("editPatientDialog").set('href' , CHOSEN_PATIENT.visitadd);
													registry.byId("editPatientDialog").set('title', "Record New Visit");
													registry.byId('editPatientDialog').show();
                        }

												if (item.name == "Visits"){
                          setUpVisitTab();
                        }

                        if (item.name == "Admissions"){
                          setUpAdmissionTab();
                        }

              }
          },
          'patientVisitTreeDiv');

          //patientVisitTree.getIconClass = setVisitTreeIcons;
          console.log("Setting Tree icons complete");

         //patientVisitTree.placeAt('patientVisitTreeDiv')
          patientVisitTree.startup();
         //patientVisitTree.expandAll();
         //patientVisitTree.collapseAll();
      });

  });
}