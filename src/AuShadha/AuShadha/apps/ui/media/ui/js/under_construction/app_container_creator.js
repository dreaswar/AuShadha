/* This creates a container for the pane and creates a basic UI with layout dijits
 * It calls the appropriate URL, receives a JSON which will have a pane attribute
 * 
 * The pane attribute has all the UI related configuration which is then parsed and 
 * UI created.
 * 
 * 
 * 
 * 
*/


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
         'dojo/parser',

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
         parser,

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

   var dijit_types = { bc     : BorderContainer,
                       tc     : TabContainer ,
                       cp     : ContentPane
   }

   var pane = {

      container:{

       /*  Holds all the info on the mainPane that is created
         * 
         * This pane will have the layouts and sub-panes along with 
         * widgets as needed
         * 
         * The information for the layout creation and widgets and sub-panes
         * will come from the constructor argument 'json'
         * 
         * --------------
         * | Attributes |
         * --------------
         *   id                : id of the container which will be the DOM id
         *   domNode           : The dom node with id of container
         *   dijit             : The main container dijit
         *   title             : Title of the container
         *   closable          : Whether container can be closed manually
         *   type              : One of the dijit_types map of the container
         *   immediateChildren : The immediateChildren dijits of the container. 
         *                       Does not include sub-children. 
       */

        id        : '',
        domNode   : '',
        dijit     : '',
        title     : '',
        closable  : true,
        type      : '',
        immediateChildren: []
      },

      _tempDomParent:'',

      widgets: {
        // a widget generator should run
        // should return the widget here
      },

      pane: {
        // a pane generator should run
        // should return the pane here
      },

      destructor: function(){
        // destroys the pane and its widgets
      },

      constructor: function( json ){
        // creates the pane and its widgets recursively
        pane._createContainer(json );

      },

      _createContainer: function (json ) {
 
        pane.container.parentDomNode = dojo.body();

        pane.container.id = json.id;
        pane.container.type = BorderContainer;
        console.log("Creating the panes and widgets");
        console.log("Received JSON: ");
        console.log(json);

        pane.container.domNode = dom.byId(pane.container.id)

        pane.container.dijit = new BorderContainer({ design: 'headline' }, "APP_LAYOUT");

        console.log("Building the widgets array ...");
        for ( var x=0; x< json.widgets.length; x++ ) {
          pane._widgetQueue.push({widget: json.widgets[x], parent: "APP_LAYOUT"});
        }
        console.log("Created the widgets array");

        console.log("Starting to create Panes...");
        for ( var x=0; x< json.panes.length; x++ ){
          pane._createPane( json.panes[x], "APP_LAYOUT" );
        }
        console.log("Created all Panes...");

        console.log("Starting to create the widgets...");
        console.log("Widget Array is : " );
        console.log(pane._widgetQueue);

        for ( var x=0; x< pane._widgetQueue.length; x++ ){
          pane._createWidget( pane._widgetQueue[x] );
        }
        pane._widgetQueue = [];
        console.log("Created all the widgets...");

        pane.container.dijit.startup();     

    },

    _widgetQueue: [],

    _createPane : function( p ,parentDomId ){

                  var paneType = dijit_types[p.type];
                  var paneDomId = p.id;
                  var paneTitle = p.title ? p.title: '';
                  var paneClosable = p.closable ? p.closable: false;
                  var paneRegion = p.region ? p.region: '';
                  var splitter = p.splitter;
                  var paneNested = p.nested ? p.nested: false;
                  var href     = p.url ? p.url: '';
                  var html = p.hrml ? p.hrml: '';

                  var hasWidgets = p.widgets;
                  var hasPanes = p.panes;

                  if ( hasWidgets ){
                    console.log( "Pushing to widget array..." );
                    for ( var x=0; x< p.widgets.length; x++ ){
                      console.log( "PUSHING: "  );
                      console.log( {widget: p.widgets[x], parent: p.id } );
                      pane._widgetQueue.push( {widget: p.widgets[x], parent: p.id } );
                    }
                    console.log( "Widget array updated.." );
                  }

                  createDom();

                  if(p.js_path){require([p.js_path])}

                  console.log( "Created all the DOMS for Pane for pane with ID: " + paneDomId );

                  if ( p.type != 'dom' ){
                    createDijit();
                  }

                  console.log( "Created all the Dijits inside pane with ID: " + paneDomId );                  

                  if ( hasPanes ) {
                    console.log( "Starting recursive Pane creation.." );
                    for ( var x=0; x< p.panes.length; x++ ){
                      pane._createPane( p.panes[x] ,p.id);
                    }
                    console.log("Finished recursive Pane creation..");                 
                  }

                  function createDom() {

                    console.log("Creating DOM with ID: " + paneDomId );

                    if ( dom.byId(paneDomId) ){
                      domConstruct.destroy( paneDomId );
                    }

                    if (! dom.byId(paneDomId) ){

                      if ( p.domType == 'img' ) {
                        domConstruct.create( p.domType,
                                            {id: paneDomId, 
                                             src: p.src,
                                             style: p.style ? p.style:'',
                                             title: p.title ? p.title: '',
                                             class: p.class ? p.class: '',
                                             alt: p.alt ? p.alt:''
                                            },
                                            p.placeAt ? p.placeAt:parentDomId,
                                            p.position ? p.position:'last'
                                           );

                        var returnValue = p.returns ? p.returns:'html';

                        if ( p.onclick ) {
                                require(["dojo/on", 
                                         "dojo/dom",
                                         "dojo/_base/xhr",
                                         "dijit/registry",
                                         "dijit/Dialog",
                                         "dojo/json"      
                                ],
                                function (on, dom, xhr, registry, Dialog, JSON) {

                                    on(dom.byId(paneDomId),
                                        "click",
                                        function () {
                                                  var myDialog = registry.byId("editPatientDialog");
                                                  xhr.get({
                                                      url: p.onclick,
                                                      load: function ( returns ) {
                                                                    if ( returnValue == 'html' ) {
                                                                      myDialog.set( 'content', returns );
                                                                      myDialog.set('title',p.title? p.title: "Dialog");
                                                                      myDialog.show();
                                                                    }
                                                                    else if (returnValue == 'json' ){
                                                                      var jsondata = JSON.parse( returns )
                                                                      if ( jsondata.success == true ){
                                                                        // Do something !! 
                                                                      }
                                                                      else {
                                                                        
                                                                      }
                                                                    }
                                                      }
                                                  });
                                        }
                                    );
                                });
                        }

                        if ( p.ondblclick ){
                          
                        }

                        if ( p.onrclick ) {
                            
                        }

                      }

                      else if ( p.domType == 'span' || p.domType == 'h3' || p.domType == 'p' ){
                        domConstruct.create(
                                          p.domType,
                                          {id: paneDomId,
                                           innerHTML: p.innerHTML ? p.innerHTML:'',
                                           class: p.class ? p.class : '',
                                           style: p.style ? p.style : '',
                                           title: p.title ? p.title : '',
                                          },
                                          p.placeAt ? p.placeAt : parentDomId,
                                          p.position ? p.position : 'last'
                                         );
                      }

                      else if ( p.domType == 'a' ){

                        domConstruct.create(
                                          p.domType,
                                          {id: paneDomId,
                                           innerHTML: p.innerHTML ? p.innerHTML:'',
                                           class: p.class ? p.class : '',
                                           style: p.style ? p.style : '',
                                           href : p.onclick ? p.onclick : '',
                                           alt: p.alt ? p.alt : '',
                                           title: p.title ? p.title : '',
                                           target: p.target ? p.target : ''
                                          },
                                          p.placeAt ? p.placeAt : parentDomId,
                                          p.position ? p.position : 'last'
                                         );

                        var returnValue = p.returns ? p.returns:'html';

                        if ( p.onclick ) {
                                require(["dojo/on", 
                                         "dojo/dom",
                                         "dojo/_base/xhr",
                                         "dijit/registry",
                                         "dijit/Dialog",
                                         "dojo/json"      
                                ],
                                function (on, dom, xhr, registry, Dialog, JSON) {

                                    on(dom.byId(paneDomId),
                                        "click",
                                        function (e) {
                                                  e.preventDefault();
                                                  var myDialog = registry.byId("editPatientDialog");
                                                  xhr.get({
                                                      url: p.onclick,
                                                      load: function ( returns ) {
                                                                    if ( returnValue == 'html' ) {
                                                                      myDialog.set( 'content', returns );
                                                                      myDialog.set('title',p.title? p.title: "Dialog");
                                                                      myDialog.show();
                                                                    }
                                                                    else if (returnValue == 'json' ){
                                                                      var jsondata = JSON.parse( returns )
                                                                      if ( jsondata.success == true ){
                                                                        // Do something !! 
                                                                      }
                                                                      else {
                                                                        
                                                                      }
                                                                    }
                                                      }
                                                  });
                                        }
                                    );
                                });
                        }

                        if ( p.ondblclick ){
                          
                        }

                        if ( p.onrclick ) {
                            
                        }

                      }

                      else {
                        domConstruct.create(
                                          'div',
                                          {id: paneDomId,
                                           innerHTML: p.innerHTML ? p.innerHTML:'',
                                           class: p.class ? p.class : '',
                                           style: p.style ? p.style : ''
                                          },
                                          p.placeAt ? p.placeAt : parentDomId,
                                          p.position ? p.position : 'last'
                                         );
                      }

                    }

                    if ( p.hasOwnProperty('class') ){
                      domClass.add( dom.byId(paneDomId), p.class );
                    }

                    if ( p.hasOwnProperty('style') ){
                      console.log("Setting Syles for " + paneDomId );
                      domStyle.set( dom.byId(paneDomId), p.style );
                      console.log("Finished Setting Syles for " + paneDomId );
                      console.log("Getting CSS Styles for : " + paneDomId );
                      console.log( domStyle.get(dom.byId(paneDomId)) ,'min-height' );
                    }

                  }


                  function createDijit() {

                    console.log("Creating Dijit with ID: " + paneDomId );

                    var paneToCreate = registry.byId( paneDomId );
                    console.log(paneDomId);
                    console.log(paneToCreate);
                    if (paneToCreate){
                      var c = paneToCreate.getChildren();
                      c.forEach(function(t){ t.destroyRecursive() });
                    }

                    if ( ! registry.byId( paneDomId ) ){

                      if ( p.type == 'cp' ) { 

                        var pd = new paneType({id: paneDomId,
                                               title: paneTitle,
                                               region: paneRegion,
                                               closable: paneClosable,
                                               splitter: splitter,
                                               style: p.style ? p.style : '',
                                               executeScripts: true,
                                               scriptHasHooks: true,
                                               parseOnLoad: true
                                            },
                                            paneDomId );

                        var html;
                        if ( href && ! p.content ){
                          request(href).then(
                            function(html){
                              pd.set('content',html);
                            },
                            function(json){
                              var jsondata = JSON.parse(json);
                              html = jsondata;
                              publishError(jsondata.error_message)
                            }
                          );
                        }
                        else if ( p.content ){
                              pd.set('content', p.content );
                        }

//                         pd.startup();
                      }

                      else if ( p.type == 'tc' ) { 
                        var pd = new paneType({id: paneDomId,
                                               region: paneRegion,
                                               splitter: splitter,
                                               tabPosition: 'top',
                                               tabStrip: true,
                                               closable: paneClosable,
                                               nested: paneNested,
                                               style: p.style ? p.style : ''
                                              },
                                              paneDomId );
//                         pd.startup();
                      }

                      else if ( p.type == 'bc' ) { 
                        var pd = new paneType({id: paneDomId,
                                               region: paneRegion,
                                               splitter: splitter,
                                               href: href,
                                               closable: paneClosable,
                                               title: paneTitle,
                                               style: p.style ? p.style : ''
                                              },
                                              paneDomId );
//                         pd.startup();
                      }

                      console.log( "Created Dijit: ");
                      console.log( pd );
                      console.log( "Adding DijitID: " + paneDomId + " as child dijit to " + parentDomId );
                      registry.byId( parentDomId ).addChild( pd );
                      console.log( "Finished creating and adding widget " );

                    }

                  }

//                   function fillData() {
//                     
//                   }

    },

    _createWidget: function( widgetQ ){

                    console.log( "Creating Widgets with Args: ");                
                    console.log( widgetQ );
                    console.log( "This widget is of type: " + widgetQ.widget.type );

                      function createDom() {

                        if (! dom.byId(widgetQ.widget.id) ){

                          if (  widgetQ.widget.type !== 'button' ) {

                            domConstruct.create('div',
                                                {id: widgetQ.widget.id},
                                                widgetQ.parent,
                                                'last');
                          }

                          else if ( widgetQ.widget.type == 'button' ) {

                            domConstruct.create('button',
                                                {id: widgetQ.widget.id, type: 'button' },
                                                 widgetQ.parent,
                                                0);

                          }

                        }

                      }

                     if ( registry.byId(widgetQ.widget.id) ) {
                       var c = registry.byId(widgetQ.widget.id);
                       console.log("Widgets Exists.. proceeding to destroy it..");
                       console.log(c);
                       c.destroyRecursive();
                     }

                        createDom();

                        console.log("Creating Widget with title: " + widgetQ.widget.title );

                        if ( widgetQ.widget.hasOwnProperty('mainTabPane') ){
                          pane.mainTabPaneDomNode = widgetQ.widget.mainTabPane;
                        }

                        if ( widgetQ.widget.type == 'tree' ){
                            require(
                              ['aushadha/tree/pane_tree_creator'],
                            function(paneTreeCreator){
                                try {
                                    paneTreeCreator(widgetQ.widget.url, 
                                                    widgetQ.widget.id, 
                                                    widgetQ.widget.mainTabPane,
                                                    widgetQ.widget.title
                                                  );
                                } 
                                catch (err){
                                    console.log(err.message);
                                }
                           });
                        }

                        else if ( widgetQ.widget.type == 'grid' ){
                            require(['aushadha/grid/generic_grid_setup',
                                    'aushadha/grid/grid_structures'],
                            function(genericGridSetup, gridStr){ 
                                try {
                                  console.log(genericGridSetup);
                                  console.log(gridStr[widgetQ.widget.str]);
                                  genericGridSetup.setupGrid(widgetQ.widget.url,
                                                            widgetQ.widget.id,
                                                            gridStr[widgetQ.widget.str],
                                                            widgetQ.widget.activateRowClick,
                                                            widgetQ.widget.title,
                                                            widgetQ.widget.storeToUse
                                  );                                      
                                } 
                                catch (err) {
                                  console.error(err);
                                }
                            });

                        }

                        else if ( widgetQ.widget.type == 'search' ){
                            var widgetStore = new JsonRest({target: widgetQ.widget.url});
                            var searchBox = new FilteringSelect({regExp        : '[a-zA-Z0-9 -]+'  ,
                                                                required       : true              ,
                                                                invalidMessage : 'No Results'      ,
                                                                store          : widgetStore       ,
                                                                searchAttr     : widgetQ.widget.searchAttr ,
                                                                labelAttr      : widgetQ.widget.labelAttr ,
                                                                labelType      : 'html'            ,
                                                                autoComplete   : widgetQ.widget.autoComplete,
                                                                placeHolder    : widgetQ.widget.placeHolder ,
                                                                hasDownArrow   : widgetQ.widget.hasDownArrow,
                                                                onChange       : function(e){
                                                                                    //widgetQ.widget.onchange
                                                                                  },
                                                                style: widgetQ.widget.style? widgetQ.widget.style: "position:relative;top: 0.1em;width: 96%;height:15%;left: 2%;"
                                                                },
                                                                widgetQ.widget.id);
//                             searchBox.startup();
                        }

                        else if ( widgetQ.widget.type == 'form' ){
                            // #TODO 
                        }

                        else if ( widgetQ.widget.type == 'button' ){
                            addButton.constructor({id: widgetQ.widget.id,
                                                  gridId: widgetQ.widget.gridId, 
                                                  label: widgetQ.widget.label,
                                                  title: widgetQ.widget.title,
                                                  url: widgetQ.widget.url
                            });
                        }

                        else if ( widgetQ.widget.type == 'something_else' ){

                        }

    }

  }

  return pane;

});
