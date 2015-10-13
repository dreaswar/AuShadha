/* GENERIC CRUD FUNCTION FOR FORM SUBMISSION - ADDING, EDITING, DELETING */

/*
A generic function to do an adding of all Items and update the div / grid accordingly
to call it with the URL , the Form's dojo-id and the grid to update and add the row to
We are assuming that the server returns a JSON with json.addData so that the row can be
updated.
*/

function addItem(url, form_id, grid_id,ADD_MORE_ITEMS) {

  require(["dojo/dom",
            "dojo/request/xhr",
            "dijit/registry",
            "dojo/json",
            "dojo/dom-form",
            "dijit/Dialog"
            ],

  function (dom, xhr, registry, JSON, domForm, Dialog) {

        var editDialog = registry.byId("editPatientDialog");
        var errorDialog = registry.byId("dialogJsonMessage");
        if (!ADD_MORE_ITEMS){ ADD_MORE_ITEMS = false; }
        xhr(url, 
            {
              handleAs: "text",
              method: "POST",
              data: domForm.toObject(form_id)
            }
        ).
        then(
            function (json) {

                var jsondata = JSON.parse(json)
                console.log(jsondata);

//                 if ( !grid_id ){
//                   var grid_id = window.CHOSEN_GRID;
//                 }

                if (jsondata.success == true) {

                    var data = jsondata.addData;                                  
//                     console.log(grid_id);
//                     console.log( window.gridStore );

                    if (grid_id){
//                        registry.byId(grid_id).store.newItem(data);
//                        registry.byId(grid_id).store.onNew();
                        registry.byId(grid_id).render();
                    }

                    dom.byId(form_id).reset();

                    publishInfo("Saved Successfully");

                    if (ADD_MORE_ITEMS == false) {
                        editDialog.hide();
                    } 
                    else {
                        registry.byId(form_id).focus();
                    }
                } 

                else {
                    errorDialog.set("title", "ERROR");
                    errorDialog.set("content", jsondata.error_message);
                    errorDialog.show();
                    publishError("ERROR ! :" + jsondata.error_message);
                }

            },
            function (json) {
                var jsondata = JSON.parse(json);
                errorDialog.set("title", "ERROR");
                errorDialog.set("content", jsondata.error_message);
                errorDialog.show();
                publishError("ERROR!: " + jsondata.error_message);
            },
            function (evt) {
                console.log(
                    "Adding Data Finished Successfully...")
            }
        );
    });
}



/*
A generic function to do an update of all Items and update the div / grid accordingly
to call it with the URL , the Form's dojo-id and the grid to update and re-render
*/

function editItem(url, form_id, grid_id) {
    
  require(
      ["dojo/request/xhr",
        "dijit/registry",
        "dojo/json",
        "dojo/dom-form",
        "dijit/Dialog"
      ],
  function (xhr, registry, JSON, domForm, Dialog) {

        var editDialog = registry.byId("editPatientDialog");
        var errorDialog = registry.byId("dialogJsonMessage");

        xhr(url, {
            handleAs: "text",
            method: "POST",
            data: domForm.toObject(form_id)
        }).
        then(
            function (json) {
                var jsondata = JSON.parse(json)
//                       console.log(jsondata);

                if (!grid_id){
                  var grid_id = window.CHOSEN_GRID
                }
                
                if (jsondata.success == true) {
                    if (grid_id ) {
                      registry.byId(grid_id).render();
                    }
                    editDialog.hide();
                    publishInfo(jsondata.error_message);
                } else {
                    errorDialog.set("title", "ERROR");
                    errorDialog.set("content", jsondata.error_message);
                    errorDialog.show();
                }
            },
            function (json) {
                var jsondata = JSON.parse(json);
                errorDialog.set("title", "ERROR");
                errorDialog.set("content", jsondata.error_message);
                errorDialog.show();
                publishError("ERROR in Server.. Please retry.");
            },
            function (evt) {
                console.log("Update Actions Finished Successfully...")
                publishInfo("Update Actions Finished Successfully...");
            }
        );
    });
}

/*
Generic Delete Function
Gets the URL to call and the Grid to update as the arguments.
*/

function delItem(url, grid_id) {

  require(["dojo/dom",
          "dojo/request/xhr",
          "dojo/json",
          "dijit/registry",
          "dijit/Dialog"
        ],

  function (dom, xhr, JSON, registry, Dialog) {

      xhr(url, {
          method: "GET",
          handleAs: "text"
      }).
      then(
          function (json) {
              var jsondata = JSON.parse(json)

              if (!grid_id){
                  var grid_id = window.CHOSEN_GRID
              }

              if (jsondata.success == true) {

                  registry.byId("editPatientDialog").hide();
                  if (grid_id ) { 
                    registry.byId(grid_id).render();
                    registry.byId(grid_id).selection.clear();
                  }
                  publishInfo("Successfully Deleted ..");

              } 

              else {
                  var errorDialog = registry.byId('dialogJsonMessage');
                  errorDialog.set('title', "ERROR!");
                  errorDialog.set('content', jsondata.error_message);
                  errorDialog.show();
              }
          },

          function (json) {
              console.log("ERROR in Server.. Please retry.");
              publishError("ERROR in Server.. Please retry.");
          },

          function (evt) {
              console.log("Deleting Item Complete")
          }

      );
  });
}
