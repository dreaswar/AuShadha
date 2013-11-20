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
    'aushadha/panes/create_tab',
    'aushadha/panes/create_form_tab',
    'aushadha/panes/create_empty_tab',
    'aushadha/panes/create_form_container',
    'aushadha/panes/create_grid_container',
    'aushadha/panes/dynamic_pane_creator',    
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
          createTab,
          createFormTab,
          createEmptyTab,
          createFormContainer,
          createGridContainer,
          createDynamicPane,
          createDynamicHTMLPane
          ){


    function onDblClickOnTree(item, mainTabPaneDomNodeId){
        require(['aushadha/under_construction/pane_and_widget_creator'],
        function(paneAndWidgetCreator){  

          if ( !item.returns || item.returns == 'json' ) {
            request( item.ondblclick ).
              then(
                function(json){
                  var jsondata = JSON.parse(json);

                  if ( item.redirect != 0 ) { 
                    // Determines whether or not to open tab in main tab 
                    // redirect if true will add the tab to the main tab 
                    // else it will add it under the main tab
                    // for main modules like OPD visits and Admission where lot of sub-tabs are 
                    // expected its better for UI purposes to open set redirect to true
                    // this can be customised in the tree.yaml 
                    paneAndWidgetCreator.constructor( jsondata.pane  );
                  }

                  else {
                    paneAndWidgetCreator.constructor( jsondata.pane , mainTabPaneDomNodeId );
                  }

                },
                function(json){
                  var jsondata = JSON.parse(json);
                  publishError(jsondata.error_message);
                }
              );
            }

          else if ( item.returns == 'html' ) {
            var args = { title: item.name[0], 
                        domId: item.id[0],
                        url: item.ondblclick[0],
                        parentTab: registry.byId(mainTabPaneDomNodeId)
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

        var mainTabPaneDomNodeId = mainTabPaneDomNode ? domAttr.get(mainTabPaneDomNode,'id'):'patient_center_tc' ;

        var gridDomId;
        
        var makeUpModuleName = function(module_string , parentName/* module | String */){
           console.log("revieved " + module_string + " to makeUpModuleName");
          var _split_string = module_string.toString().split('_');
          var module_name = [];

          if (! parentName){
            var y ={parent: mainTabPaneDomNodeId,module_name:''}; 
          }
          else{
            var y ={parent:parentName.toString(),module_name:''}; 
          }

          for(var i=0; i< (_split_string.length-1); i++){ 
              module_name.push( _split_string[i] ); 
              console.log(module_name);
          }; 

          y.module_name = module_name.join('_');
           console.log(y);
          return y;
        }

        function makeTabConstructorArgument(module,item){
            var tabArgs = { 
              parent: module.parent,
              module_type:item.type,
              module_label:module.module_name,

              widgets_allowed: ['grid','button'],

              dom:{id: module.parent + '_' + module.module_name +'_cp',
                    parent: module.parent ,
                    title : "Add " + item.name
              },

              grid:{id: mainTabPaneDomNodeId+"_"+module.module_name + '_list',
                    url:CHOSEN_PATIENT.urls.json[module.module_name],
                    str: GRID_STRUCTURES[module.module_name.toUpperCase()]
              },

              button:{label: 'Add', 
                      title: "Add "+ item.name,
                      url : CHOSEN_PATIENT.urls.add[module.module_name]
              }
            }

            console.log(tabArgs);
            gridDomId = mainTabPaneDomNodeId+"_"+module.module_name + '_list';            
            return tabArgs;
        }

        function makeTheTab(item,parentName, makeContainer){
            var item = item;

            if(item.type != 'application'){
              var module = makeUpModuleName(item.type, parentName);
            }

            else{
              var module = makeUpModuleName(item.module_type, parentName);
            } 

            var tabArgs = makeTabConstructorArgument(module, item);

            if(! makeContainer){

              var tab_parent = registry.byId(tabArgs.dom.parent)
              var tab_dijit = registry.byId(tabArgs.dom.id);

              if(! tab_dijit){
                  createTab.constructor(tabArgs);
              }
              else{
                  tab_parent.selectChild(tab_dijit);
              }

            }

            else{
                return createGridContainer.constructor(tabArgs);
            }
        }

        var tree = new Tree({model   : treeModel,
                             showRoot: false,
                             onDblClick: function(item,node,evt){

                                            if (! item.ondblclick ) {
                                              var formLayout = (['form']).sort().toString();
                                              var gridLayout = (['grid','button']).sort().toString();

//                                               if(item.ui_layout == 'standard'){
// 
//                                                 var widgets = item.widgets.sort().toString() ;
// 
//                                                 var obj={parent: mainTabPaneDomNodeId ,
//                                                         module_name: (item.module_name).toString(),
//                                                         module_title: (item.name).toString()
//                                                 };
// 
//                                                 var formArgs={parent: mainTabPaneDomNodeId ,
//                                                               module_name: (item.module_name).toString(),
//                                                               module_title: (item.name).toString(),
//                                                               url:CHOSEN_PATIENT.urls.add[ item.module_name.toString() ]
//                                                       };
// 
//                                                 var emptyTab = createEmptyTab.constructor(obj);
//                                                 emptyTab.addBc('vertical',1);
//                                                 var parentNode = domAttr.get(emptyTab.pane.Bc.topCp.domNode,'id')
// 
//                                                 if (widgets == gridLayout ){
//                                                    emptyTab.pane.Bc.
//                                                     topCp.
//                                                     addChild( 
//                                                         makeTheTab(item,
//                                                                    parentNode,
//                                                                    true
//                                                                   )
//                                                     );
//                                                 }
// 
//                                                 else if(widgets == formLayout ){
//                                                   emptyTab.pane.Bc.
//                                                     topCp.
//                                                     addChild( 
//                                                         createFormContainer.constructor(formArgs) 
//                                                     );
//                                                 }
// 
//                                                 else{
//                                                   alert("This is an unimplemented widget arrangement !! ");
//                                                   return false;
//                                                 }
// 
//                                                 emptyTab.pane.startup();
//                                                 var p = emptyTab.pane.getParent(); 
//                                                 p.selectChild(emptyTab.pane);
// 
//                                               }
// 
//                                               else if (item.ui_layout == 'composite'){
// 
//                                                   var p_widget_layout = item.widgets.sort().toString();
// 
//                                                   var obj={parent: mainTabPaneDomNodeId,
//                                                            module_name: item.module_name.toString(),
//                                                            module_title: item.name.toString(),
//                                                   };
// 
//                                                   var emptyTab = createEmptyTab.constructor(obj);
// 
//                                                   console.log("Creating vertical layout");
//                                                   emptyTab.addBc('vertical',3);
// 
//                                                   if (p_widget_layout == formLayout ) {
//                                                     var formArgs={ parentPane: emptyTab.pane,
//                                                                    module_name: item.module_name.toString(),
//                                                                    module_title: item.name.toString(),
//                                                                    url:CHOSEN_PATIENT.urls.add[ item.module_name.toString() ]
//                                                     };
//                                                     emptyTab.pane.Bc.topCp.addChild( createFormContainer.constructor(formArgs) );
//                                                   }
// 
//                                                   else if(p_widget_layout == gridLayout ){
//                                                     var parentNode = domAttr.get(emptyTab.pane.Bc.topCp.domNode,'id')
//                                                     emptyTab.pane.Bc.topCp.addChild( makeTheTab(item,
//                                                                                                 parentNode,
//                                                                                                 true)
//                                                                                    );
//                                                   }
// 
//                                                   console.log("Trying to create a SubTabcontainer");
//                                                   console.log("Existing Content panes are: ");
//                                                   console.log(emptyTab.pane.Bc.topCp);
//                                                   console.log(emptyTab.pane.Bc.bottomCp);
// 
//                                                   var linkedTc = TabContainer({tabStrip:true,
//                                                                                tabPosition:'top',
//                                                                                style: "height: 100%; width: 400px; overflow: auto;"
//                                                                               },
//                                                                               domConstruct.create('div',{id: item.module_name.toString()+"_subTc"},
//                                                                                                   emptyTab.pane.Bc.bottomCp.domNode,
//                                                                                                   'last')
//                                                                              );
// 
//                                                   for (var x=0; x< item.linked_modules.length; x++){
// 
//                                                       var linked_widget_layout = item.linked_modules[x].widgets.sort().toString();
//                                                       console.log(linkedTc);
//                                                       var parentName = domAttr.get(linkedTc.domNode, 'id').toString();
// 
//                                                       if (linked_widget_layout == gridLayout ){
//                                                         var theTab = makeTheTab(item.linked_modules[x],
//                                                                                       parentName,
//                                                                                       true
//                                                                                      ) 
//                                                         console.log(theTab);
//                                                         linkedTc.addChild(theTab);
//                                                       }
//                                                       else if (linked_widget_layout ==  formLayout ) {
//                                                         var linkedModuleFormArgs = {
//                                                           parentPane: linkedTc,
//                                                           module_name: linked_modules[x].module_name.toString(),
//                                                           module_title: linked_modules[x].name.toString(),
//                                                           url: CHOSEN_PATIENT.urls.add[ linked_modules[x].module_name.toString()]
//                                                         }
//                                                         linkedTc.addChild( createFormContainer.constructor(linkedModuleFormArgs) );
//                                                       }
// 
//                                                   }
//                                                   linkedTc.startup();
//                                                   emptyTab.pane.Bc.bottomCp.addChild(linkedTc);
// 
//                                                   emptyTab.pane.startup();
//                                                   var p = emptyTab.pane.getParent(); 
//                                                   p.selectChild(emptyTab.pane);
//                                               }
// 
//                                               else if ( item.ui_layout == 'pane'){
// 
//                                                 var query = '?patient_id='+CHOSEN_PATIENT.id;
//                                                 var paneUrl = '/AuShadha/visit/visit/pane/'+query;
// 
//                                                 request( paneUrl ).
//                                                 then( 
// 
//                                                   function( json ) { 
//                                                       var jsondata= JSON.parse(json);
//                                                       console.log(jsondata);
//                                                       createDynamicPane(jsondata);
//                                                   },
// 
//                                                   function( json ){
//                                                     var jsondata= JSON.parse(json);                                                    
//                                                     publishError(jsondata.error_message);
//                                                   }
// 
//                                                 );
//                                               }
// 
//                                             }
// 
//                                             else{
// 
//                                               var urlToCall = item.ondblclick;
//                                               var redirectAfterClick = item.redirect;
//                                               var allChildrenTabs = registry.byId(mainTabPaneDomNodeId).getChildren();
//                                               var lastChild = allChildrenTabs[allChildrenTabs.length-1];
//                                               var domId = item.id.toString().replace(' ','_').toLowerCase();
// 
//                                               var args = { title: item.name, 
//                                                             domId: domId,
//                                                             url: urlToCall,
//                                                             parentTab: registry.byId(mainTabPaneDomNodeId)
//                                                         };
// 
//                                               if ( redirectAfterClick == 1 ) {
// 
//                                                 console.log("Creating Dynamic HTML Pane with Arguments: ");
//                                                 console.log(args);
//                                                 createDynamicHTMLPane( args );
// 
//                                               }
// 
//                                               else{
//                                                 request(urlToCall).then(
// 
//                                                   function(json){
//                                                     var jsondata = JSON.parse(json);
//                                                     if (jsondata.success = true) {
//                                                        console.log(tree);
//                                                        tree.refresh();
//                                                        publishInfo(jsondata.error_message);
//                                                     }
//                                                     else{
//                                                       publishError(jsondata.error_message);
//                                                     }
//                                                   },
// 
//                                                   function(json) {
//                                                     var jsondata = JSON.parse(json);
//                                                     publishError(jsondata.error_message);
//                                                   }
// 
//                                                 );
//                                               }
//                                             }
                                        }

                                        else{
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