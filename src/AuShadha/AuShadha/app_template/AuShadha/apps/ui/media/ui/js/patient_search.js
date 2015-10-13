
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
