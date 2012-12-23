function(urlObj /* URL Object */){
	require([
					"dojo/dom",
					"dojo/dom-style",
					"dojo/dom-construct",

					"dijit/registry",
					"dijit/form/Button",
					"dojox/layout/ContentPane",
					"dijit/layout/TabContainer",
					"dijit/layout/BorderContainer",
	], 
	function(dom, 
					 domStyle, 
					 domConstruct, 
					 registry, 
					 Button,
					 ContentPane, 
					 TabContainer, 
					 BorderContainer){
		
		function makeDoms(){
			domConstruct.create('div',
													{id: "patientObstetricsPreventivesTab"},
													"patientPreventiveTabs",
													"last"
			);

					domConstruct.create('div',
															{id: "obstetric_history_detail"},
															"patientObstetricsPreventivesTab",
															"first"
					);
		}

		function makeDijits(){
		  var preventiveHealthTabs  =  registry.byId('prenventiveHealthTabs');
			var patientObstetricsPreventivesTab = new ContentPane({id:"patientObstetricsPreventivesTab",
                                                        title:"Obstetrics"
                                                        },
                                                        "patientObstetricsPreventivesTab"
                                                        );
      preventiveHealthTabs.addChild(patientObstetricsPreventivesTab);

					var patientObstetricsHistoryDetail = new ContentPane({id:"obstetric_history_detail",
																											},
																											"obstetric_history_detail"
																											);
					patientObstetricsPreventivesTab.addChild(patientObstetricsHistoryDetail);
		
					registry.byId('obstetric_history_detail').set('href',urlObj.obstetricHistoryUrl);
					registry.byId('preventiveHealthTabs').
						selectChild( registry.byId('obstetric_history_detail') )
			
		}

		makeDoms();
		makeDijits();

});

}