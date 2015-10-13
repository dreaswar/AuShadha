/*
 * Workhorse module for creation of Panes, Widgets and Layouts 
 * 
 * Retrieves a JSON from a URL after AJAX and parses the pane attribute of the JSON
 * This attribute has all the configuration for setting up the pane UI and enclosing widgets
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

   // Currently these are the container types allowed. This can be expanded to cover all the layout options
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

      constructor: function( json, parentTab, redirectToMainTab ){

        /* 
         * Workhorse function which does the creation of everything UI
         * creates the pane and its widgets recursively
         */

        // Check for additional DOJO modules that may be provided and insert that into dojoConfig at runtime
        if ( json.dojoConfig ) {
          for ( var x=0; x< json.dojoConfig.length; x++ ) {
            dojoConfig.packages.push(json.dojoConfig[x]);
            require( json.dojoConfig[x] );
          }
        }
        else {
          console.log("djConfig not set for additional modules. Scripts if any will not load from them");
        }

        if ( parentTab ){
          // Sets the parent TabContainer
          // This will determine where the container is created 
          // We would want a parent to attach children to
          pane.parentTab = parentTab;
        }

        if (! redirectToMainTab ){
          // Attaching children to parent tab container is assumed.
          // In case you want to override specify it here 
          // int 0 and 1 are allowed
          // Skipping assumes it is 1
          console.log("No redirect specified. Assuming redirection to main tab")
          redirectToMainTab  = 1;
        }

        // Proceed with container creation
        pane._createContainer(json, redirectToMainTab );

      },

      _createContainer: function (json /* JSON */, 
                                  redirectToMainTab /* int 0/1 */) {
 
        // The default grandParents 
        pane.container.grandParentDomNode = dom.byId('centerTopTabPane');
        pane.container.grandParentDijit = registry.byId('centerTopTabPane');

        // If you are attaching DOMS under the main tab DOM Node ie.. the centerTopTabPane
        if ( redirectToMainTab == 1 ) {
          pane.container.parentDomNode = dom.byId('centerTopTabPane');
          pane.container.parentDijit = registry.byId('centerTopTabPane');
        }

        // If else you want to specify your own attaching point
        else if ( redirectToMainTab == 0 ) {
          pane.container.parentDomNode = dom.byId(pane.parentTab);
          pane.container.parentDijit = registry.byId(pane.parentTab);
        }

        // Just in case
        else {
          alert("This redirect directive will not work now.... Currently directives of 0 or 1 are supported ")
        }


        pane.container.id = json.id;                                                           // This is the DOM element ID
        pane.container.title = json.title;                                                     // This is the title of the Dijit generated
        pane.container.type = dijit_types[json.type] ? dijit_types[json.type]: BorderContainer;// If skipped assumed that you want to create BC
//         console.log("Creating the panes and widgets");
//         console.log("Received JSON: ");
//         console.log(json);

        // Check for the presence of the container with same id and destroy the widgets
        if ( registry.byId( pane.container.id ) ) {

            try {
              pane.container.parentDijit.removeChild( registry.byId( pane.container.id ) );
              registry.byId( pane.container.id ).destroyRecursive();
            } 
            catch (err) {
              console.log(err.message);
            }

        }

        // destroy the DOM element as well if it exists
        if ( dom.byId( pane.container.id ) ) {
          domConstruct.destroy( dom.byId( pane.container.id ) );
        }


        // Create the DOM node under parentDomNode as the last DOM element
        pane.container.domNode = domConstruct.create('div',
                                                      { id: pane.container.id },
                                                      pane.container.parentDomNode,
                                                      'last'
                                                    );

        // Dijitise the container
        pane.container.dijit = new pane.container.type({ id: pane.container.id, 
                                                           closable: json.closable ? json.closable: false, 
                                                           title: pane.container.title,
                                                           scriptHasHooks: true,
                                                           executeScripts: true
                                                        },
                                                        pane.container.id);

        // Add this Dijit to the parentDijit and call startup
        pane.container.parentDijit.addChild( pane.container.dijit );
        pane.container.dijit.startup();
        pane.container.parentDijit.resize();

//         pane.container.grandParentDijit.selectChild( pane.container.parentDijit);
//         pane.container.parentDijit.selectChild( registry.byId( pane.container.id ) )

//         console.log("Building the widgets array ...");

        // Proceed with Widget creation
        // A widget queue is created first
        for ( var x=0; x< json.widgets.length; x++ ) {
          pane._widgetQueue.push({widget: json.widgets[x], parent: pane.container.id});
        }

//         console.log("Created the widgets array");
//         console.log("Starting to create Panes...");

        // Create Layout widget from the pane attribute of the json returned
        for ( var x=0; x< json.panes.length; x++ ){
          pane._createPane( json.panes[x], pane.container.id );
        }

//         console.log("Created all Panes...");
//         console.log("Starting to create the widgets...");
//         console.log("Widget Array is : " );
//         console.log(pane._widgetQueue);

        // Iterate through the widgetQ and create widgets
        for ( var x=0; x< pane._widgetQueue.length; x++ ){
          pane._createWidget( pane._widgetQueue[x] );
        }
        pane._widgetQueue = [];

//         console.log("Created all the widgets...");

        // Select the dijit after all widgets, panes are created
        pane.container.parentDijit.selectChild(pane.container.dijit);

    },

    _widgetQueue: [], // an empty widgetQ array

    _createPane : function( p ,parentDomId ){

                  var paneType = dijit_types[p.type];                      // Type of pane to create
                  var paneDomId = p.id;                                    // DOM ID of the pane
                  var paneTitle = p.title ? p.title: '';                   // Title of the Dijit
                  var paneClosable = p.closable ? p.closable: false;       // closable attribute in case of tabbed pane
                  var paneRegion = p.region ? p.region: '';                // Region setting in case of layout containers
                  var splitter = p.splitter;                               // Whether splitter is allowed
                  var paneNested = p.nested ? p.nested: false;             // Whether tabs are displayed in nested way
                  var href     = p.url ? p.url: '';                        // the href attribute 
                  var html = p.hrml ? p.hrml: '';                          // Direct content attribute

                  var hasWidgets = p.widgets;                              // Find out whether there are enclosed widgets
                  var hasPanes = p.panes;                                  // Find out whether there are nested panes

                  // If it has nested widgets add them to the queue
                  if ( hasWidgets ){
//                     console.log( "Pushing to widget array..." );
                    for ( var x=0; x< p.widgets.length; x++ ){
//                       console.log( "PUSHING: "  );
//                       console.log( {widget: p.widgets[x], parent: p.id } );
                      pane._widgetQueue.push( {widget: p.widgets[x], parent: p.id } );
                    }
//                     console.log( "Widget array updated.." );
                  }

                  createDom();                                              // Create the DOM elements
//                   console.log( "Created all the DOMS for Pane for pane with ID: " + paneDomId );

                  // Load the JS from js_path
                  if (p.js_path){ require([p.js_path])}   

                  // If the element does not create a widget ie.. type== dom or domType is set then create a dijit
                  if ( p.type != 'dom' ){
                    createDijit();
                  }

//                   console.log( "Created all the Dijits inside pane with ID: " + paneDomId );                  

                  // Create recursive panes
                  if ( hasPanes ) {
//                     console.log( "Starting recursive Pane creation.." );
                    for ( var x=0; x< p.panes.length; x++ ){
                      pane._createPane( p.panes[x] ,p.id);
                    }
//                     console.log("Finished recursive Pane creation..");                 
                  }

                  // Defines the function to create DOM elements
                  function createDom() {

//                     console.log("Creating DOM with ID: " + paneDomId );

                    if ( dom.byId(paneDomId) ){
                      domConstruct.destroy( paneDomId );
                    }

                    if (! dom.byId(paneDomId) ){

                      // If the DOM element is an img
                      if ( p.domType == 'img' ) {
                        domConstruct.create( p.domType,
                                            {id    : paneDomId, 
                                             src   : p.src,
                                             style : p.style ? p.style:'',
                                             title : p.title ? p.title: '',
                                             class : p.class ? p.class: '',
                                             alt   : p.alt ? p.alt:''
                                            },
                                            p.placeAt ? p.placeAt:parentDomId,
                                            p.position ? p.position:'last'
                                           );
                        
                        var returnValue = p.returns ? p.returns:'html';

                        // Bind an click event if specified to the DOM NODE
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
                                                                        // Do Something else !! 
                                                                      }
                                                                    }
                                                      }
                                                  });
                                        }
                                    );
                                });
                        }

                        // Bind the dblclick event
                        if ( p.ondblclick ){

                        }

                        // Bind the Right Click event
                        if ( p.onrclick ) {

                        }

                      }

                      // If DOM type is not img 
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

                      // if DOM type is a
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

                      // If nothing is specified about DOM type create a div
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

                    // Specify the CSS class
                    if ( p.hasOwnProperty('class') ){
                      domClass.add( dom.byId(paneDomId), p.class );
                    }

                    // Specify the CSS style
                    if ( p.hasOwnProperty('style') ){
                      domStyle.set( dom.byId(paneDomId), p.style );
//                       console.log("Setting Syles for " + paneDomId );
//                       console.log("Finished Setting Syles for " + paneDomId );
//                       console.log("Getting CSS Styles for : " + paneDomId );
//                       console.log( domStyle.get(dom.byId(paneDomId)) ,'min-height' );
                    }

                  }


                  // The function to create Dijits
                  function createDijit() {

//                     console.log("Creating Dijit with ID: " + paneDomId );

                    var paneToCreate = registry.byId( paneDomId );
//                     console.log(paneDomId);
//                     console.log(paneToCreate);
                    if (paneToCreate){
                      var c = paneToCreate.getChildren();
                      c.forEach(function(t){ t.destroyRecursive() });
                    }
//                     debugger;

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

                        pd.startup();
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
                        pd.startup();
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
                        pd.startup();
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

//                     console.log( "Creating Widgets with Args: ");                
//                     console.log( widgetQ );
//                     console.log( "This widget is of type: " + widgetQ.widget.type );

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
//                        console.log("Widgets Exists.. proceeding to destroy it..");
//                        console.log(c);
                       c.destroyRecursive();
                     }

                        createDom();

//                         console.log("Creating Widget with title: " + widgetQ.widget.title );

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

                          if (! widgetQ.widget.gridStrModule ) {

                            require(['aushadha/grid/generic_grid_setup',
                                    'aushadha/grid/grid_structures'],

                              function(genericGridSetup, gridStr){ 

                                try {
//                                   console.log(genericGridSetup);
//                                   console.log(gridStr[widgetQ.widget.str]);
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

                          else {

                            require(dojoConfig, 
                                    ['aushadha/grid/generic_grid_setup',
                                      widgetQ.widget.gridStrModule
                                    ],

                              function(genericGridSetup, gridStr){ 

                                try {
//                                   console.log(genericGridSetup);
//                                   console.log(gridStr[widgetQ.widget.str]);
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
                        }

                        else if ( widgetQ.widget.type == 'dynamic_pane_grid' ){
                            
                            require(['aushadha/grid/generic_grid_setup',
                                     'aushadha/grid/grid_structures'
                                    ],
                            
                            function(genericGridSetup, gridStr){ 
                            
                              try {
//                                   console.log(genericGridSetup);
//                                   console.log(gridStr[widgetQ.widget.str]);
                                  genericGridSetup.setupDynamicPaneGrid(widgetQ.widget.url,
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
                            searchBox.startup();
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

                        else if ( widgetQ.widget.type == 'custom_widget' ){

                              require(dojoConfig,
                                      [widgetQ.widget.js_path], 
                              function(w) { 
                                  console.log(widgetQ.widget.args);
                                  w(widgetQ.widget.args);  
                              });

                        }

    }

  }

  return pane;

});
