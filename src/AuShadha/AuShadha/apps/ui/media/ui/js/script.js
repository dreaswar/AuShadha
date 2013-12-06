  require([
          "dojo/dom",
          "dojo/_base/xhr",
          "dojox/grid/DataGrid",
          "dojo/store/JsonRest",
          "dojox/data/JsonRestStore",
          "dojo/data/ObjectStore",
          "dojo/on",
          "dijit/registry",
          "dijit/Dialog",
          "dojo/ready",
          "dojo/_base/array",
          "dojo/dom-construct",
          "dojo/dom-style",
          "dojox/layout/ContentPane",
          "dojo/behavior",
          "dojo/store/Memory",
          "dojo/dom-geometry",
          "dojo/request",
          "dojo/_base/fx",
          'dojo/parser',

          'aushadha/main',
          'aushadha/panes/create',

            "dojo/_base/connect",
            "dijit/TitlePane",
            "dijit/layout/TabContainer",
            "dijit/layout/BorderContainer",
            "dijit/layout/SplitContainer",
            "dijit/Editor",
            "dijit/form/Form",
            "dijit/form/Button",
            "dijit/form/TextBox",
            "dijit/form/ValidationTextBox",
            "dijit/form/Textarea",
            "dijit/form/SimpleTextarea",
            "dijit/form/DateTextBox",
            "dijit/form/TimeTextBox",
            "dijit/form/NumberTextBox",
            "dijit/form/NumberSpinner",
            "dijit/form/Select",
            "dijit/form/MultiSelect",
            "dijit/form/FilteringSelect",
            "dojox/form/Manager",
            "dojox/validate/web",
            "dijit/Tooltip",
            "dijit/Tree",
            "dojo/store/Observable",
            "dijit/dijit",
            "dojox/widget/Toaster",
            "dijit/Menu",
            "dijit/MenuBar",
            "dijit/PopupMenuBarItem",
            "dijit/DropDownMenu",
            "dijit/MenuItem",
            "dojo/data/ItemFileWriteStore",
            "dojox/data/QueryReadStore",
            "dojo/domReady!"
  ],

  function (dom,
      xhr,
      DataGrid,
      JsonRest,
      JsonRestStore,
      ObjectStore,
      on,
      registry,
      Dialog,
      ready,
      array,
      domConstruct,
      domStyle,
      ContentPane,
      behaviour,
      Memory,
      domGeom,
      request,
      fx,
      parser,

      auMain,
      auCreatePane
  ) {

        // Define Variables to be used later in the app..

        ready(function () {
          console.log("Starting script script.js");

            /* Attach Basic CRUD functions for Patient Addition */

//                   function addNewPatient() {
//                       require(["dojo/_base/xhr",
//                               "dijit/registry",
//                               "dijit/Dialog"
//                       ],
//                       function (xhr, registry, Dialog) {
//                           var myDialog = registry.byId(
//                               "editPatientDialog");
//                           xhr.get({
//                               url: PAT_NEW_ADD_URL,
//                               load: function (html) {
//                                   myDialog.set('content', html);
//                                   myDialog.set('title',
//                                       "Enroll New Patient to the Clinic"
//                                   );
//                                   myDialog.show();
//                               }
//                           });
//                       });
//                   }
// 
//                   //{% if perms.patient.add_patientdetail %}
//                   var addPatientButton = new dijit.form.Button({
//                           label: "New",
//                           iconClass: "addPatientIcon_32",
//                           onClick: function () {
//                               addNewPatient();
//                           }
//                       },
//                       "addPatientButton");
// 
//                   require(["dojo/on", "dojo/dom"],
//                       function (on, dom) {
//                           on(dom.byId("addPatientButtonSmall"),
//                               "click",
//                               function () {
//                                   addNewPatient();
//                               }
//                           );
//                       });
//                   //{% endif %}
// 
//                   var patientIdStore = new JsonRest({
//                       target: "{%url patient_id_autocompleter %}",
//                       idProperty: 'patient_id'
//                   });
// 
//                   var patientHospitalIdStore = new JsonRest({
//                       target: "{%url patient_hospital_id_autocompleter  %}",
//                       idProperty: 'patient_id'
//                   });
// 
//                   var patientNameStore = new JsonRest({
//                       target: "{%url patient_name_autocompleter %}",
//                       idProperty: 'patient_id'
//                   });
// 
// 
//                   var patientHospitalIdSelect = new dijit.form.FilteringSelect({
//                           label: "Search Patient ID: ",
//                           name: "patientHospitalIdAutoCompleter",
//                           store: patientHospitalIdStore,
//                           autoComplete: false,
//                           required: true,
//                           placeHolder: "Search Patient ID.",
//                           hasDownArrow: true,
//                           style: "width: 175px; margin-left: 20px;",
//                           searchAttr: "patient_hospital_id",
//                           labelAttr: "name",
//                           onChange: function (patient_hospital_id) {
//                               console.log("You chose " + this.item.patient_hospital_id)
//                               console.log("You chose Patient: " + this.item
//                                   .patient_name)
//                               if (this.item == false) {
//                                   dojo.attr(dojo.byId(
//                                           "patientSearchFormSubmitBtn"),
//                                       'disabled',
//                                       'disabled'
//                                   )
//                               }
//                               if (this.item) {
//                                   dojo.attr(dojo.byId(
//                                           "patientSearchFormSubmitBtn"),
//                                       'disabled', '')
//                                   console.log(patientHospitalIdStore)
//                                   console.log(this.item.patient_hospital_id)
//                                   var queryItem = patientHospitalIdStore.
//                                   query({
//                                       "patient_hospital_id": this.item.patient_hospital_id
//                                   })
//                                   var get_name = this.item.patient_name +
//                                       ""
//                                   var patNameItem = patientNameStore.
//                                   query({
//                                       "patient_name": this.item.patient_name,
//                                       "patient_id": this.item.patient_id
//                                   });
//                                   dijit.byId("patientNameSelection")
//                                       .
//                                   set('displayedValue', this.item.patient_name);
//                                   var patient_id = this.item.patient_id;
//                                   var searchedPatientId = myStore.query({
//                                       'patient_id': patient_id
//                                   });
//                                   grid.filter({
//                                       id: patient_id
//                                   }, true);
//                                   console.log(searchedPatientId);
//                                   //                            alert(searchedPatientId.results )
//                                   //                            var myStorePatient = grid.store.fetchItemByIdentity({"patient_id":patient_id})
//                                   //                            console.log(myStorePatient)
//                               }
//                           }
//                       },
//                       "patientHospitalIdSelection"
//                   );
// 
//                   patientHospitalIdSelect.startup();
// 
//                   var patientNameSelect = new dijit.form.FilteringSelect({
//                           label: "Search Patient Name ",
//                           name: "patientNameAutoCompleter",
//                           store: patientNameStore,
//                           autoComplete: false,
//                           required: true,
//                           placeHolder: "Search Patient Name",
//                           hasDownArrow: true,
//                           labelAttr: "patient_name",
//                           style: "width: 175px; margin-left: 20px;",
//                           searchAttr: "patient_name",
//                           onChange: function (patient_name) {
//                               //                            alert("You chose " + this.item.patient_hospital_id)
//                               if (this.item) {
//                                   //                              alert(this.item.patient_id)
//                                   var queryItem = patientHospitalIdStore.
//                                   query({
//                                       'patient_hospital_id': this.item.patient_hospital_id
//                                   });
// 
//                                   dijit.byId("patientHospitalIdSelection")
//                                       .
//                                   set('displayedValue', this.item.patient_hospital_id);
//                                   /*
//                         dijit.byId("patientIdSelection").
//                          set('displayedValue', queryItem.patient_hospital_id);
// */
//                               }
//                           }
//                       },
//                       "patientNameSelection"
//                   );
// 
//                   patientNameSelect.startup();



            /* Hide the Loader */
            var fadeAwayLoader = fx.fadeOut({
                node: dom.byId('aushadhaLoaderIndicator'),
                duration: 3300
            });

            on( fadeAwayLoader,
                "End",
                function () {
                    domStyle.set(dom.byId('aushadhaLoaderIndicator'), {display: 'none'} );
                }, 
                true
            );

            require(['dojo/request',
              'dojo/dom',
              'dojo/parser',
              'dojo/ready',
              'dojo/json',
              'dijit/registry',
              'aushadha/under_construction/app_container_creator',
              'dojo/domReady!'
              ],

            function(request,dom,parser,ready,JSON,registry,appContainerCreator){

              ready(

              function(){

                  request( URL_render_aushadha_ui_pane ).
                  then(

                    function(json){
                      var jsondata = JSON.parse(json);
                      var pane = jsondata.pane;
                      appContainerCreator.constructor( pane );
                      console.log("Getting The Installed Apps from script.js");
                      getInstalledApps();
                      fadeAwayLoader.play();
                      console.log("Finished running the Animations and Fading it..");
                      parser.parse('tooltipsAndDialogs');                      
                    },

                    function(json){
                      var jsondata = JSON.parse(json);
                      alert("ERROR! UI could not be loaded");
                      console.error(jsondata.error_message);
                    }

                  );
                }
              );

            });

    });

    function getInstalledApps() {
        request( URL_installed_apps /* Variable from urls.js */ ).
        then(
          function( json ){
            var jsondata = JSON.parse(json);
            if ( jsondata.success == true ){
              console.log(jsondata.installed_apps);
              console.log(jsondata.UI);
              window.INSTALLED_APPS = jsondata.installed_apps;
              window.UI = jsondata.UI;
              auCreatePane(); 
            }
            else{
              publishError(jsondata.error_message);
            }
          },

          function( json ){
            var jsondata = JSON.parse(json);
            publishError(jsondata.error_message);
          },

          function(evt){
            console.log(evt);
            publishError(evt);
          }
        );
    }

});
  
