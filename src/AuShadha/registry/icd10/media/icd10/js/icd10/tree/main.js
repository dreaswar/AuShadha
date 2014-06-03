define([
         'dojo/window',
         "dojo/store/Memory",
         "dijit/tree/ObjectStoreModel",
         "dijit/Tree",
         "dijit/tree/ForestStoreModel",
         "dojo/data/ItemFileReadStore",

         'dojo/dom',
         'dojo/on',
         'dojo/request',
         'dojo/json',
         'dojo/dom-construct',
         'dojo/dom-style',
         'dojo/dom-class',
         'dojo/dom-attr',
         'dojo/ready',
         'dojo/parser',
         'dijit/registry',
         'dojo/query',
         'dojo/NodeList-traverse',
         'dojo/NodeList-data',
         'dojo/domReady!'
        ],

function(win,
         Memory,
         ObjectStore,
         Tree,
         ForestStoreModel,
         ItemFileReadStore,
         dom,
         on,
         request,
         JSON,
         domConstruct, 
         domStyle, 
         domClass, 
         domAttr, 
         ready, 
         parser, 
         registry,
         query) {

    var mainTabPane, treeRootTitle;
    var defaultTreeTitle = 'ICD10 Tree';
    var treeContainerBcDomId = 'ICD10_CENTER_BC';
    var treeDomIds = ['ICD10_LEADING_CP_TREE','ICD10_SECTION_TREE','ICD10_DIAGNOSIS_TREE'];

    var buildTree = function (args) {
        var url = args.url;
        var domNode = args.id;
        mainTabPane = args.mainTabPane? args.mainTabPane: 'PATIENT_CENTER_CP_TC';
        treeRootTitle = args.title?args.title: defaultTreeTitle;

        // Create the store
        var treeStore = new ItemFileReadStore({url: url,
                                              clearOnClose:true,
                                              heirarchial:false
        });

        // Create the model
        var treeModel = new ForestStoreModel({store         : treeStore,
                                              query         : {type: 'application'},
                                              rootId        : 'root',
                                              rootLabel     : treeRootTitle? treeRootTitle.toString(): defaultTreeTitle,
                                              childrenAttrs : ["children"]
                                              });
        // Create the tree
        var tree = new Tree({model: treeModel, showRoot: false},domNode);
        tree.on('dblclick', onTreeDblClick);
        tree.startup();
        tree.collapseAll();

        // Define the refresh & refreshModel methods
        tree.refresh = function() {
		var treeStore = new ItemFileReadStore({url: url,
							clearOnClose:true,
							heirarchial:false
		});

		tree.model.store = treeStore;
		tree.model.query = {"type": "application"};
		tree.rootId = "root";
		tree.rootLabel = treeRootTitle? treeRootTitle.toString(): defaultTreeTitle,
		tree.childrenAttrs = ["children"];
		tree.refreshModel();
         }

	 tree.refreshModel = function() {
	        // reset the itemNodes Map
		tree._itemNodesMap = {};
		// reset the state of the rootNode
		tree.rootNode.state = "UNCHECKED";
		// Nullify the tree.model's root-children
		tree.model.root.children = null;
		// remove the rootNode
		if ( tree.rootNode) {
		   tree.rootNode.destroyRecursive();
		}
		// reload the tree
		tree._load();
	 }


    }

    // Create a factory which returns
    var treeMaker = function(args) {
      buildTree(args);
    }


    // Define the dblclick handler
    function onTreeDblClick(item) {
        var url = item.ondblclick[0];
        var targetNodeId = item.target_node[0];

        // If the dblclick event returns a widget and it is of the type 'custom_tree_widget'
        if (item.returns[0] == 'widget' && item.widget_type[0] == 'custom_tree_widget') {
		var indexOfTarget = treeDomIds.indexOf(targetNodeId);

                // Prepare the DOM. Removes the trees after the clicked tree
		for (var i=0; i<treeDomIds.length; i++) { 
                  if ( registry.byId(treeDomIds[i]) ) {
                     var nodeIndex = treeDomIds.indexOf(treeDomIds[i]);
                     if ( indexOfTarget != -1 && nodeIndex  >= indexOfTarget ) {
		       parent_dom =  query( "#"+treeDomIds[i]).parents('.widgetContainer')[0];
		       target_node_type = query( "#"+treeDomIds[i])[0].tagName.toLowerCase();
		       registry.byId(treeDomIds[i]).destroyRecursive(false);
		       domConstruct.create(target_node_type, { id: treeDomIds[i] }, parent_dom, 0 );
		     }
                 
                  }
                }

                // Make the new tree
                treeMaker({url: url, id: targetNodeId, mainTabPane: mainTabPane, title: treeRootTitle });

        } 

        // Incase the dblclick wants to return html
        else if (item.returns[0] == 'html') {
          request(url).then(
              function(html) {
                 registry.byId(targetNodeId).set('content', html);
              });
        }

    }

    // Return the factory
    return treeMaker;
});
