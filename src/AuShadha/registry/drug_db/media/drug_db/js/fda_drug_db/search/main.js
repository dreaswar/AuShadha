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

         'aushadha/panes/dynamic_html_pane_creator', 
         'aushadha/panes/create_add_button',

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


       var searchWidget = function(args) {
		    var widgetStore = new JsonRest({target: args.url});
		    var searchBox = new FilteringSelect({regExp        : '[a-zA-Z0-9 -]+'  ,
							required       : true              ,
							invalidMessage : 'No Results'      ,
							store          : widgetStore       ,
							searchAttr     : args.searchAttr ,
							labelAttr      : args.labelAttr ,
							labelType      : 'html'            ,
							autoComplete   : args.autoComplete,
							placeHolder    : args.placeHolder ,
							hasDownArrow   : args.hasDownArrow,
							onChange       : function(e){
                                                                            registry.byId('FDA_DRUG_SUMMARY_CP').set('href',this.item.url);
                                                                            if (registry.byId("FDA_DRUG_DB_GRID")) {
                                                                                registry.byId("FDA_DRUG_DB_GRID").selection.clear();
                                                                            }
									  },
							style: args.style? args.style: "position:relative;top: 0.1em;width: 96%;height:15%;left: 2%;"
							},
							args.id);
		    searchBox.startup();
         }
         return searchWidget;
});
