define([
                "dojo/dom",
                "dojo/dom-style",
      "dojo/query",
                "dojo/dom-construct",

                "dijit/registry",
                "dijit/form/Button",
                "dojox/layout/ContentPane",
                "dijit/layout/TabContainer",
                "dijit/layout/BorderContainer",
], 
function(dom, 
        domStyle,
        query,
        domConstruct, 
        registry, 
        Button,
        ContentPane, 
        TabContainer, 
        BorderContainer){

		function makeDoms(){

			domConstruct.create('div',
                                {id:"contactAndDemographicsTab"},
                                'patientSummaryTab',
                                "after"
			);
			domStyle.set('contactAndDemographicsTab',{"height":"auto","overflow":"auto"});
					domConstruct.create('div',
                                        {id: "demographics_add_or_edit_form"},
                                        "contactAndDemographicsTab",
                                        "first"
					);

          domStyle.set('demographics_add_or_edit_form',{height:"30em"});

					domConstruct.create("div",
                                          {"id":"contact_tab_container"},
                                      'demographics_add_or_edit_form',
                                      "after"
					);

					domConstruct.create("div",
                                        {"id":"contact_list_container"},
                                      'contact_tab_container',
                                      "first"
						);
						domConstruct.create("div",
                                            {"id":"contact_list"},
                                          'contact_list_container',
                                          "first"
							);
					domConstruct.create("div",
                                        {"id":"phone_list_container"},
                                      'contact_list_container',
                                      'after'
						);
						domConstruct.create("div",
                                            {"id":"phone_list"},
                                          'phone_list_container',
                                          'first'
						);
					domConstruct.create('div',
                                        {id: "guardian_list_container"},
                                        "phone_list_container",
                                        "after"
						);
						domConstruct.create('div',
                                            {id: "guardian_list"},
                                            "guardian_list_container",
                                            "first"
						);
		}

		function makeDijits(urlObj){
			
			var demographicsTab = new ContentPane({ title     : "Demographics",
                                                    closable  : true,
                                                    iconClass : "contactIcon"
                                                },
                                                "contactAndDemographicsTab"
			);
			registry.byId('patientContextTabs').addChild(demographicsTab);

			var demographicsAddOrEditForm = new ContentPane({
                                                              id:"demographics_add_or_edit_form",
                                                              href: urlObj.demographicsUrl
                                              },	
                                              "demographics_add_or_edit_form"
                                              );
			demographicsTab.addChild(demographicsAddOrEditForm);
			var contactTabs = new TabContainer({
														id: "contact_tab_container",
														tabPosition:"bottom",
														tabStrip:true,
														tolayout:true,
														useSlider:true,
														style:"position:relative; height: 25em; width: 45em; overflow:auto;"
													},
													"contact_tab_container"
			);
			demographicsTab.addChild(contactTabs);
			var contactListPane = new ContentPane({id:"contact_list_container",
																							title: "Address"
																			},
																			"contact_list_container"
																			);
			contactTabs.addChild(contactListPane);
			setupContactGrid(urlObj.contactUrl);
			var phoneListPane   = new ContentPane({id:"phone_list_container",
																							title : "Phone"
																			},
																			"phone_list_container"
																			);
			contactTabs.addChild(phoneListPane);
			setupPhoneGrid(urlObj.phoneUrl,'phone_list',GRID_STRUCTURES.PATIENT_PHONE_GRID_STRUCTURE);
			var guardianListPane    = new ContentPane({id:"guardian_list_container",
													  title : "Guardian"
                                                      },
                                                      "guardian_list_container"
										);
			contactTabs.addChild(guardianListPane);
			setupGuardianGrid(urlObj.guardianUrl);

			demographicsTab.startup();

			registry.byId("patientContextTabs").selectChild("contactAndDemographicsTab");
			registry.byId("patientTabsBorderContainer").resize();

		}

		function makeButtons(){
		//{% if perms.patient.add_patientcontact %}
    var addContactButton =  new Button({
                                  label: "Add",
                                  title: "Add New Contact Details",
                                  iconClass: "addPatientContactIcon_16",
                                  onClick: function(){
                                            require(["dojo/_base/xhr", "dojo/_base/array"],
                                            function(xhr, array){
                                                xhr.get({
                                                        url: "{%url contact_json %}"+
                                                             "?patient_id="+
                                                             dom.byId("selected_patient_id_info").innerHTML +
                                                             "&action=add",
                                                        load: function(html){
                                                                      var myDialog = dijit.byId("editPatientDialog");
                                                                      myDialog.set('content', html);
                                                                      myDialog.set('title', "Add Postal Address Information");
                                                                      myDialog.show();
                                                              }
                                                 });
                                            });
                                 }
                              },
                              domConstruct.create('button',
                                                  {type : "button",
                                                   id   : "addContactButton"
                                                  },
                                                  "contact_list",
                                                  "before"
                              )
    );

		//{% endif %}


		//{% if perms.patient.add_patientphone %}

    var addPhoneButton =  new Button({
                                    label: "Add",
                                    title: "Add New Phone Numbers",
                                    iconClass: "addPatientPhoneIcon_16",
                                    onClick: function(){
                                           require(
                                            ["dojo/_base/xhr", "dojo/_base/array"],
                                            function(xhr, array){
                                              xhr.get({
                                                url: "{%url phone_json %}"+"?patient_id="+
                                                       dom.byId("selected_patient_id_info").innerHTML +
                                                      "&action=add",
                                                load: function(html){
                                                             var myDialog = dijit.byId("editPatientDialog");
                                                             myDialog.set('content', html);
                                                             myDialog.set('title', "Add Phone Numbers");
                                                             myDialog.show();
                                                       }
                                             });
                                           })
                                    }
                         },
                         domConstruct.create('button',
                                            {type :"button",
                                             id   :"addPhoneButton"
                                            },
                                            "phone_list",
                                            "before"
                         )
		);

		//{% endif %}

		//{%if perms.patient.add_patientguardian %}
    var addGuardianButton =  new Button({
                                        label: "Add",
                                        title:"Add Guardian Details",
                                        iconClass: "dijitIconNewTask",
                                        onClick: function(){
                                               require(
                                                ["dojo/_base/xhr", "dojo/_base/array"],
                                                function(xhr, array){
                                                  xhr.get({
                                                    url: "{%url guardian_json %}"+"?patient_id="+
                                                          dom.byId("selected_patient_id_info").innerHTML +
                                                          "&action=add",
                                                    load: function(html){
                                                             var myDialog = dijit.byId("editPatientDialog");
                                                             myDialog.set('content', html);
                                                             myDialog.set('title', "Add Guardian Information ");
                                                             myDialog.show();
                                                          }
                                                 });
                                               })
                                        }
                         },
                         domConstruct.create('button',
                                              {type : "button",
                                               id   : "addGuardianButton"
                                              },
                                              "guardian_list",
                                              "before")
    );
		//{% endif %}

	}

    return {
        constructor: function (urlObj){
                        makeDoms();
                        makeDijits(urlObj);
                        makeButtons();
                     };
    }

});