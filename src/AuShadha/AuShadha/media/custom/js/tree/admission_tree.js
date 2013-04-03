function buildAdmissionTree(){
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
      "dojo/dom-construct",
      "dojo/dom-style",

      "dojo/json"
  ], 
  function(ready, 
           win,

           Memory, 
           ObjectStoreModel,
           Tree,
           ForestStoreModel,
           ItemFileReadStore,
           
           dom, 
           registry,
           domConstruct, 
           domStyle, 

           JSON ){

    var existingTree = registry.byId('patientAdmissionTreeDiv');

     if(existingTree){
       console.log("Tree exists.. proceeding to destroy it..")
       existingTree.destroyRecursive();
     }

     console.log(registry.byId("patientAdmissionTreeDiv"));
     if(!dom.byId("patientAdmissionTreeDiv")){
        domConstruct.create('div',
                            {id: "patientAdmissionTreeDiv"},
                            "patientAdmissionTreeContainer",
                            "first"
        );
        domStyle.set( dom.byId('patientAdmissionTreeDiv'),{'minWidth':'200px',
                                                  'maxWidth':'300px',
                                                  'minHeight':"400px",
                                                  'overflow':"auto"
        });
    }

     // Create store
/*
     var patientAdmissionTreeStore = new ItemFileReadStore({url: CHOSEN_PATIENT.patientAdmissionTreeUrl,
                                                        clearOnClose:true,
                                                        heirarchial:false
    });
    console.log(patientAdmissionTreeStore);
     // Create the model
      var patientAdmissionTreeModel = new ForestStoreModel({
          store: patientAdmissionTreeStore,
          query: {type: 'application'},
          rootId: 'root',
          rootLabel:"Admission",
          childrenAttrs:["children"]
      });
*/


      var patientAdmissionTreeStore = new Memory({
          data: [
              { id: 'admission',
                name:'Admission',
                type:'trunk'
              },

                { id: 'investigations',
                  name:'Investigations',
                  type:'main_branch',
                  parent: 'admission'
                },
                { id: 'imaging',
                  name:'Imaging',
                  type:'main_branch',
                  parent: 'admission'
                },

                { id: 'patient_media',
                  name:'Media',
                  type:'main_branch',
                  parent: 'admission'
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
                      parent: 'patient_media'
                    }

          ],
          getChildren: function(object){
              return this.query({parent: object.id});
          }

      });

      // Create the model
      var patientAdmissionTreeModel = new ObjectStoreModel({
          store: patientAdmissionTreeStore,
          query: {id: 'admission'},
          labelAttr: "name"
      });


      // Create the Tree.
      ready(function(){

          function setAdmissionTreeIcons(item, opened){
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

          var patientAdmissionTree = new Tree({
              model   : patientAdmissionTreeModel,
              showRoot: false,
              onClick: function(item){

                        if (item.name == "Visits"){
                          setUpAdmissionTab();
                        }

                        if (item.name == "Admissions"){
                          setUpAdmissionTab();
                        }

              }
          },
          'patientAdmissionTreeDiv');

//           patientAdmissionTree.getIconClass = setAdmissionTreeIcons;
          console.log("Setting Tree icons complete");

         //patientAdmissionTree.placeAt('patientAdmissionTreeDiv')
          patientAdmissionTree.startup();
         //patientAdmissionTree.expandAll();
         //patientAdmissionTree.collapseAll();
      });

  });
}