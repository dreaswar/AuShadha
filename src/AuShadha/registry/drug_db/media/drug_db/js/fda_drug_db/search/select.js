define(
        ['dojo/dom',
         'dojo/dom-construct',
         'dojo/dom-class',
         'dojo/dom-style',
         'dojo/dom-attr',
         'dojo/ready',
         'dojo/query',
         "dojo/request",
         "dojo/json",

	 'dijit/registry',
         'dojo/parser',
         'dijit/layout/BorderContainer',
         'dijit/layout/TabContainer',
         'dojox/layout/ContentPane',
         'dijit/form/Button',
         'dijit/Tree',

         'dijit/form/FilteringSelect',
         'dijit/form/Select',

         "dojo/store/JsonRest",
         "dojo/data/ObjectStore",

         'dojo/NodeList-data',
         'dojo/NodeList-traverse',

         "dijit/form/Form"
        ],

function(
         dom,
         domConstruct,
         domClass,
         domStyle,
         domAttr,
         ready,
         query,
         request,
         JSON,

         registry,
         parser,
         BorderContainer,
         TabContainer,
         ContentPane,
         Button,
         Tree,
         
         FilteringSelect,
         Select,
         JsonRest,
         ObjectStore,

         dynamicHTMLPaneCreator,
         addButton
      ){

       var drugDbSearchWidget = registry.byId('DRUG_DB_SEARCH_WIDGET');
       
       var searchWidget = function(args) {
		    var searchBox = new Select({ name: args.name, options: args.options }, args.id);
		    searchBox.onChange = function(e) { 
			                      for (var x=0; x< args.options.length; x++ ) {
						   if (args.options[x].value == e) { 
                                                       var url = args.options[x].url;
						       drugDbSearchWidget.set('store',null);
			                               var widgetStore = new JsonRest({target: url});
  						       drugDbSearchWidget.set('store',widgetStore);
					      	   };
			                      }
			                 };
		    searchBox.startup();
        }
      return searchWidget;
});
