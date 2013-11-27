define([
    'dojo/window',
    "dojo/store/Memory",
    "dijit/tree/ObjectStoreModel",
    "dijit/Tree",
    "dijit/tree/ForestStoreModel",
    "dojo/data/ItemFileReadStore",

    "dojo/dom",
    "dijit/registry",
    "dojo/dom-construct",
    "dojo/dom-style",
    'dojo/dom-attr',
    "dojo/json",

    'dojox/fx/scroll',

    'dojo/query',
    'dojo/request',

    "dijit/registry",
    "dojox/layout/ContentPane",
    "dijit/layout/BorderContainer",
    "dijit/layout/TabContainer",

    'aushadha/grid/grid_structures',
    'aushadha/panes/dynamic_html_pane_creator'

  ], 

  function(win,
          Memory, 
          ObjectStoreModel,
          Tree,
          ForestStoreModel,
          ItemFileReadStore,
          dom, 
          registry,
          domConstruct, 
          domStyle, 
          domAttr,
          JSON,
          scroll,
          query,
          request,

          registry,
          ContentPane,
          BorderContainer,
          TabContainer,

          GRID_STRUCTURES,
          createDynamicHTMLPane

          ){


    function onDblClickOnTree(item, mainTabPaneDomNodeId){
        require(['aushadha/under_construction/pane_and_widget_creator'],
        function(paneAndWidgetCreator){

          if ( !item.returns || item.returns[0] == 'json' ) {

            request( item.ondblclick ).
            then(
                function( json ){
                  var redirect = item.redirect ? item.redirect[0]:false;
                  var jsondata = JSON.parse(json);

                  if ( redirect == 1 ) { 
                    // Determines whether or not to open tab in main tab 
                    // redirect if true will add the tab to the main tab 
                    // else it will add it under the main tab
                    // for main modules like OPD visits and Admission where lot of sub-tabs are 
                    // expected its better for UI purposes to open set redirect to true
                    // this can be customised in the tree.yaml 
                    paneAndWidgetCreator.constructor( jsondata.pane  );
                  }

                  else if ( redirect == 0 ) {
                    paneAndWidgetCreator.constructor( jsondata.pane , mainTabPaneDomNodeId );
                  }

                  else if ( !redirect ) {
                    alert("this requires a custom handler")
                  }

                },

                function(json){
                  var jsondata = JSON.parse(json);
                  publishError(jsondata.error_message);
                }
              );
            }

          else if ( item.returns[0] == 'html' ) {
            var args = { title: item.name[0], 
                         domId: item.id[0],
                         url: item.ondblclick[0],
                         parentTab: registry.byId( mainTabPaneDomNodeId )
                    };              
            console.log(args);
            createDynamicHTMLPane( args );
          }

        });
    }

    var buildTree = function (url,domNode, mainTabPaneDomNode,treeRootTitle) {

        var treeStore = new ItemFileReadStore({url: url,
                                              clearOnClose:true,
                                              heirarchial:false
        });

        // Create the model
        var treeModel = new ForestStoreModel({store         : treeStore,
                                              query         : {type: 'application'},
                                              rootId        : 'root',
                                              rootLabel     : treeRootTitle? treeRootTitle.toString():"Patient",
                                              childrenAttrs : ["children"]
                                              });

        var mainTabPaneDomNodeId = mainTabPaneDomNode ? domAttr.get(mainTabPaneDomNode,'id'): false ;

        var tree = new Tree({model   : treeModel,
                             showRoot: false,
                             onDblClick: function(item,node,evt){

                                            if ( item.ondblclick ) {
                                              onDblClickOnTree(item, mainTabPaneDomNodeId);
                                            }

                                }
                            },
                            domNode);

        tree.startup();
//      tree.expandAll();
        tree.collapseAll();

        tree.refresh = function(){
          var treeStore = new ItemFileReadStore({url: url,
                                                clearOnClose:true,
                                                heirarchial:false
          });

          tree.model.store = treeStore;
          tree.model.query = {"type": "application"};
          tree.rootId = "root";
          tree.rootLabel = treeRootTitle? treeRootTitle.toString():"Patient",
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

    return buildTree;

});