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
      'dojo/request',

      'aushadha/panes/visit_pane',
      'aushadha/panes/visit_edit_pane'
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
            JSON,
            request,

            VISIT_PANE,
            VISIT_EDIT_PANE
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
          onClick: function(item){
                    if (item.id == 'NEW_OPD_VISIT'){
                      
                    }
                    if (item.type == 'visit'){
                      
                    }
                    if (item.id == 'MEDICATION_LIST'){
                      
                    }
                    if (item.id == 'INV'){
                      
                    }
                    if (item.id =='IMAG'){
                      
                    }
          },
          onDblClick: function(item){

                    if (item.id =='NEW_OPD_VISIT'){
                      request(item.addUrl).then(
                        function(html){
                          try{
                            VISIT_PANE.addPane.constructor({id    : "NEW_VISIT_TAB", 
                                                         title  : "Add Visit",
                                                         content: html});
                          }catch(err){
                            console.error(err.message);
                          }
                        },
                        function(err){
                          publishError(err);
                        }
                      );
                    }

                    if (item.type=='visit' || item.type == 'fu_visit'){
                      request(item.editUrl).then(
                        function(html){
                          VISIT_PANE.editPane.constructor({id     : item.id, 
                                                          title   : "Edit: " + item.name, 
                                                          content : html}
                                                         );
                        },
                        function(err){
                          publishError(err);
                        }
                      );
                    }

                    if (item.type=='visit_follow_up_add'){
                      request(item.addUrl).then(
                        function(html){
                          alert(item.id);
                          VISIT_PANE.addPane.constructor({id     : item.id, 
                                                          title   : "Add: " + item.name, 
                                                          content : html}
                                                         );
                        },
                        function(err){
                          publishError(err);
                        }
                      );
                    }

                    if (item.id =='MEDICATION_LIST'){
                      request(CHOSEN_PATIENT.visitsummary).then(
                        function(html){
                          alert("Feature Not Implemented yet. When its done, Medication List will load in a new tab");
                        },
                        function(err){
                          publishError(err);
                        }
                      );
                    }

                    if (item.id =='INV' || item.id == 'IMAG'){
                      request(CHOSEN_PATIENT.visitsummary).then(
                        function(html){
                          alert("Feature Not Implemented yet. When its done, Labs will load in a new tab");
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