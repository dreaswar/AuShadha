require(["dojo/on",
         "dijit/registry",
         "dojo/keys",
         "dijit/Dialog",
         "dijit/form/ComboBox",
         "dijit/form/FilteringSelect",
         "dijit/form/Button",
         "dojo/store/Memory",
         "dojo/dom-construct",
         "dojo/request",
         "dojo/dom",
         "dojo/json",

         "aushadha/grid/generic_grid_setup",
         'aushadha/grid/grid_structures',

         "dojo/domReady!"
        ],
    function (on,
        registry,
        keys,
        Dialog,
        ComboBox,
        FilteringSelect,
        Button,
        Memory,
        domConstruct,
        request,
        dom,
        JSON,
        GRID_SETUP,
        GRID_STRUCTURES) {

        on(document.body, "keyup", function (e) {

            console.log(e);
            console.log(keys);

            var setupPopUpGrid = GRID_SETUP.setupPopUpGrid;

            function createDomsAndDijits(action, urlStore) {

                if (registry.byId('addChoiceFilteringSelect')) {
                    registry.byId('addChoiceFilteringSelect')
                        .destroyRecursive();
                }
                if (registry.byId('addChoiceSubmitButton')) {
                    registry.byId('addChoiceSubmitButton')
                        .destroyRecursive();
                }

                domConstruct.create("div", {
                    id: "addDialogContentDiv"
                }, "addDialogContent", "first");
                domConstruct.create("div", {
                    id: "addChoiceFilteringSelect"
                }, "addDialogContentDiv", 0);
                domConstruct.create("input", {
                        id: "addChoiceSubmitButton",
                        name: "addChoiceSubmitButton",
                        type: 'button',
                        value: 'Go>'
                    },
                    "addDialogContentDiv", 1
                );

                var filteringSelect = new FilteringSelect({
                    name: "addChoiceFilteringSelect",
                    value: "",
                    store: urlStore,
                    searchAttr: "name",
                    hasDownArrow: false,
                    autoComplete: true,
                    onBlur: function (e) {
                        var urlToCall = this.get('value');
                        if (urlToCall) {
                            console.log("Calling URL " + urlToCall);
                            registry.byId('addChoiceSubmitButton')
                                .focus();
                        } else {
                            return false;
                        }
                    }
                }, "addChoiceFilteringSelect");

                var submitButton = new Button({
                    id: 'addChoiceSubmitButton',
                    label: "Go >> ",
                    onClick: function (e) {
                        var urlToCall = registry.byId(
                            'addChoiceFilteringSelect')
                            .get('value');
                        var chosenValue = registry.byId(
                            'addChoiceFilteringSelect')
                            .get('displayedValue');
                        if (urlToCall) {
                            request(urlToCall)
                                .then(
                                    function (html) {
                                        registry.byId('addDialog')
                                            .hide();
                                        if (urlToCall == CHOSEN_PATIENT
                                            .contactjson ||
                                            urlToCall == CHOSEN_PATIENT
                                            .phonejson ||
                                            urlToCall == CHOSEN_PATIENT
                                            .guardianjson ||
                                            urlToCall == CHOSEN_PATIENT
                                            .admissionjson ||
                                            urlToCall == CHOSEN_PATIENT
                                            .visitjson ||
                                            urlToCall == CHOSEN_PATIENT
                                            .medicationlistjson ||
                                            urlToCall == CHOSEN_PATIENT
                                            .allergiesjson ||
                                            urlToCall == CHOSEN_PATIENT
                                            .medicalhistoryjson ||
                                            urlToCall == CHOSEN_PATIENT
                                            .surgicalhistoryjson ||
                                            urlToCall == CHOSEN_PATIENT
                                            .familyhistoryjson ||
                                            urlToCall == CHOSEN_PATIENT
                                            .immunisationjson
                                        ) {
                                            console.log(
                                                "Trying to create a Grid Popup..."
                                            )
                                            var storeItem = urlStore.get(
                                                urlToCall);
                                            var gridStr = storeItem.gridStr;
                                            var gridHtml = storeItem.gridFn(
                                                urlToCall, gridStr,
                                                'gridDialogContent');
                                            registry.byId('gridDialog')
                                                .show();
                                        } else {
                                            if (chosenValue == 'Visit' &&
                                                action == 'Add') {
                                                if (registry.byId(
                                                    'newVisitAddForm'
                                                )) {
                                                    registry.byId(
                                                        'newVisitAddForm'
                                                    )
                                                        .destroyRecursive();
                                                }
                                            }
                                            var thisDialog = new Dialog({
                                                content: html,
                                                title: action
                                            });
                                            thisDialog.onClose =
                                                function () {
                                                    this.destroyRecursive();
                                            }
                                            thisDialog.onHide =
                                                function () {
                                                    this.destroyRecursive();
                                            }
                                            thisDialog.show();
                                            /*
                                                                registry.byId('editPatientDialog').set('content',html);
                                                                registry.byId('editPatientDialog').set('title',action);
                                                                registry.byId('editPatientDialog').show();
                                                                */
                                        }
                                    },
                                    function (error) {
                                        publishError("ERROR! " + error);
                                        registry.byId(
                                            'addChoiceFilteringSelect')
                                            .set('displayedValue', '');
                                        registry.byId(
                                            'addChoiceFilteringSelect')
                                            .focus();
                                    }
                            );
                        } else {
                            registry.byId('addChoiceFilteringSelect')
                                .focus();
                            return false;
                        }
                    }
                }, "addChoiceSubmitButton");
                filteringSelect.startup();
                submitButton.startup();
                registry.byId("addDialog")
                    .set('title', action);
                registry.byId("addDialog")
                    .show();
            }

            if (e.altKey && e.keyCode == 76) {

                if (CHOSEN_PATIENT) {

                    if (registry.byId('patientHomeContentPane')
                        .get('selected') ||
                        registry.byId('admissionHomeContentPane')
                        .get('selected') ||
                        registry.byId('visitHomeContentPane')
                        .get('selected')) {

                        var listUrlStore = new Memory({
                            data: [

                                                //{% if perms.patient.add_patientcontact %} //
                                {
                                    name: "Contact",
                                    id: CHOSEN_PATIENT.contactjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_CONTACT_GRID_STRUCTURE
                                },
                                                //{% endif %}//

                                                //{% if perms.patient.add_patientphone %}
                                {
                                    name: "Phone",
                                    id: CHOSEN_PATIENT.phonejson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_PHONE_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientguardian %}
                                {
                                    name: "Guardian",
                                    id: CHOSEN_PATIENT.guardianjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_GUARDIAN_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.admission.add_admission %}
                                {
                                    name: "Admission",
                                    id: CHOSEN_PATIENT.admissionjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_ADMISSION_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.visit.add_visitdetail %}
                                {
                                    name: "Visit",
                                    id: CHOSEN_PATIENT.visitjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_VISIT_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientmedicationlist %}
                                {
                                    name: "Medication List",
                                    id: CHOSEN_PATIENT.medicationlistjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_MEDICATION_LIST_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientallergy %}
                                {
                                    name: "Allergy",
                                    id: CHOSEN_PATIENT.allergiesjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_ALLERGIES_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientmedia %}
                                {
                                    name: "Media",
                                    id: "/",
                                    gridFn: setupPopUpGrid,
                                    gridStr: null
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientfamilyhistory %}
                                {
                                    name: "Family History",
                                    id: CHOSEN_PATIENT.familyhistoryjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_FAMILY_HISTORY_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientsocialhistory %}
                                {
                                    name: "Social History",
                                    id: CHOSEN_PATIENT.socialhistoryjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_SOCIAL_HISTORY_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientmedicalhistory %}
                                {
                                    name: "Medical History",
                                    id: CHOSEN_PATIENT.medicalhistoryjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_MEDICAL_HISTORY_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientimmunisation %}
                                {
                                    name: "Immunisation History",
                                    id: CHOSEN_PATIENT.immunisationjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_IMMUNIZATION_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientsurgicalhistory %}
                                {
                                    name: "Surgical History",
                                    id: CHOSEN_PATIENT.surgicalhistoryjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_SURGICAL_HISTORY_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.obs_and_gyn.add_obstetrichistorydetail %}
                                {
                                    name: "Obstetric History",
                                    id: CHOSEN_PATIENT.obstetrichistorydetailjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_OBSTETRIC_HISTORY_DETAIL_GRID_STRUCTURE
                                },
                                                //{% endif %}

                                                //{% if perms.patient.patientdemographics %}
                                {
                                    name: "Demographics",
                                    id: CHOSEN_PATIENT.demographicsjson,
                                    gridFn: setupPopUpGrid,
                                    gridStr: GRID_STRUCTURES.PATIENT_DEMOGRAPHICS_GRID_STRUCTURE
                                }
                                                //{% endif %}
                                         ]
                        });
                        createDomsAndDijits('List', listUrlStore);
                    }
                }
            }


            if (e.keyCode == keys.INSERT || (e.altKey && e.keyCode == 73)) {
                if (CHOSEN_PATIENT) {

                    if (registry.byId('patientHomeContentPane')
                        .get('selected') ||
                        registry.byId('admissionHomeContentPane')
                        .get('selected') ||
                        registry.byId('visitHomeContentPane')
                        .get('selected')) {

                        var addUrlStore = new Memory({
                            data: [
                                                //{% if perms.patient.add_patientcontact %} //
                                {
                                    name: "Patient",
                                    id: "{%url 'patient_detail_add_without_id' %}"
                                },
                                                //{% endif %}//

                                                //{% if perms.patient.add_patientcontact %} //
                                {
                                    name: "Contact",
                                    id: CHOSEN_PATIENT.contactadd
                                },
                                                //{% endif %}//

                                                //{% if perms.patient.add_patientphone %}
                                {
                                    name: "Phone",
                                    id: CHOSEN_PATIENT.phoneadd
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientguardian %}
                                {
                                    name: "Guardian",
                                    id: CHOSEN_PATIENT.guardianadd
                                },
                                                //{% endif %}

                                                //{% if perms.admission.add_admission %}
                                {
                                    name: "Admission",
                                    id: CHOSEN_PATIENT.admissionadd
                                },
                                                //{% endif %}

                                                //{% if perms.visit.add_visitdetail %}
                                {
                                    name: "Visit",
                                    id: CHOSEN_PATIENT.visitadd
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientmedicationlist %}
                                {
                                    name: "Medication List",
                                    id: CHOSEN_PATIENT.medicationlistadd
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientallergy %}
                                {
                                    name: "Allergy",
                                    id: CHOSEN_PATIENT.allergiesadd
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientmedia %}
                                {
                                    name: "Media",
                                    id: "/"
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientfamilyhistory %}
                                {
                                    name: "Family History",
                                    id: CHOSEN_PATIENT.familyhistoryadd
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientsocialhistory %}
                                {
                                    name: "Social History",
                                    id: CHOSEN_PATIENT.socialhistoryadd
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientmedicalhistory %}
                                {
                                    name: "Medical History",
                                    id: CHOSEN_PATIENT.medicalhistoryadd
                                },
                                                //{% endif %} 

                                                //{% if perms.patient.add_patientimmunisation %}
                                {
                                    name: "Immunisation History",
                                    id: CHOSEN_PATIENT.immunisationadd
                                },
                                                //{% endif %}

                                                //{% if perms.patient.add_patientsurgicalhistory %}
                                {
                                    name: "Surgical History",
                                    id: CHOSEN_PATIENT.surgicalhistoryadd
                                },
                                                //{% endif %}

                                                //{% if perms.obs_and_gyn.add_obstetrichistorydetail %}
                                {
                                    name: "Obstetric History",
                                    id: CHOSEN_PATIENT.obstetrichistorydetailadd
                                },
                                                //{% endif %}

                                                //{% if perms.patient.patientdemographics %}
                                {
                                    name: "Demographics",
                                    id: CHOSEN_PATIENT.demographicsadd
                                }
                                                //{% endif %}
                                            ]
                        });
                        createDomsAndDijits('Add', addUrlStore);
                    }
                } else {
                    //{% if perms.patient and perms.add_patientdetails %}
                    request("{%url 'patient_detail_add_without_id' %}")
                        .then(
                            function (html) {
                                var thisDialog = new Dialog({
                                    content: html,
                                    title: 'Add'
                                });
                                thisDialog.onClose = function () {
                                    this.destroyRecursive();
                                }
                                thisDialog.onHide = function () {
                                    this.destroyRecursive();
                                }
                                thisDialog.show();
                                /*
                registry.byId('editPatientDialog').set('content',html);
                registry.byId('editPatientDialog').set('title',"Add New Patient");
                registry.byId('editPatientDialog').show();
                */
                            },
                            function (error) {
                                publishError("ERROR! " + error);
                            }
                    );
                    //{% else %}
                    return false;
                    //{% endif %}
                }
            } else {
                console.log(e);
            }
        })
    });