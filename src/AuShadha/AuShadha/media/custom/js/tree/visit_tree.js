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
      "dojo/dom-construct",
      "dojo/dom-style",
      "dojo/json",
      'dojo/request'
      
//       ,'aushadha/panes/visit_edit_pane',
  ], function(ready, 
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
              JSON,
              request
//               ,VISIT_EDIT_PANE
             ){

      var existingTree = registry.byId('visitLSidebarTreeDiv');

      if(existingTree){
        console.log("Tree exists.. proceeding to destroy it..")
        existingTree.destroyRecursive();
      }

      console.log(registry.byId("visitLSidebarTreeDiv"));
      if(!dom.byId("visitLSidebarTreeDiv")){
          domConstruct.create('div',
                              {id: "visitLSidebarTreeDiv"},
                              "visitLSidebarTreeContainer",
                              "first"
          );
          domStyle.set( dom.byId('visitLSidebarTreeDiv'),
                        {'minWidth' : '200px',
                        'maxWidth' : '300px',
                        'minHeight': "400px",
                        'overflow' : "auto"
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
          store          : patientVisitTreeStore,
          query          : {type: 'application'},
          rootId         : 'root',
          rootLabel      : "OPD Visits",
          childrenAttrs  : ["children"]
      });

      // Create the Tree.
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
          onDblClick: function(item){
                    if (item.id=='NEW_OPD_VISIT'){
                      request(item.addUrl).then(
                        function(html){
                          registry.byId('editPatientDialog').set('content',html);
                          registry.byId('editPatientDialog').set('title',"New Visit: " + CHOSEN_PATIENT.full_name);
                          registry.byId('editPatientDialog').show();
                        },
                        function(err){
                          publishError(err);
                        }
                      );
                    }
                    if (item.type=='visit'){
                      request(item.editUrl).then(
                        function(html){
                          registry.byId('editPatientDialog').set('content',html);
                          registry.byId('editPatientDialog').set('title',"Edit Visit: " + CHOSEN_PATIENT.full_name);
                          registry.byId('editPatientDialog').show();
//                           console.log(VISIT_EDIT_PANE);
//                           VISIT_EDIT_PANE.constructor(html);
                        },
                        function(err){
                          publishError(err);
                        }
                      );
                    }
          }
      },
      'visitLSidebarTreeDiv');

      //patientVisitTree.getIconClass = setVisitTreeIcons;
      console.log("Setting Visit Tree icons complete");

      patientVisitTree.startup();
      patientVisitTree.expandAll();

  });
}