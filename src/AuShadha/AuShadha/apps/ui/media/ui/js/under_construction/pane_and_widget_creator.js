/*//////////////////////////////////////////////////////////////////////////////
 * 
 * 
 * 
 * 
 * 
*///////////////////////////////////////////////////////////////////////////////


define(
        ['dojo/dom',
         'dojo/dom-construct',
         'dojo/dom-class',
         'dojo/dom-style',
         'dojo/dom-attr',
         'dojo/ready',
         'dojo/query',

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

         'aushadha/panes/dynamic_pane_creator',
         'aushadha/panes/dynamic_html_pane_creator', 
         'aushadha/panes/create_main_pane',
         'aushadha/panes/create_add_button',

         'dojo/NodeList-data',
         'dojo/NodeList-traverse'
        ],

function(
         dom,
         domConstruct,
         domClass,
         domStyle,
         domAttr,
         ready,
         query,

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

         dynamicPaneCreator,
         dynamicHTMLPaneCreator,
         createMainPane,
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

      constructor: function( json, parentTab ){
        // creates the pane and its widgets recursively
        if (parentTab){
          pane.parentTab = parentTab;
        }
        pane._createContainer(json);

      },

      _createContainer: function (json) {
 
        if (! pane.parentTab ){
          pane.container.parentDomNode = dom.byId('centerTopTabPane');
          pane.container.parentDijit = registry.byId('centerTopTabPane');
        }
        else{
          pane.container.parentDomNode = dom.byId(pane.parentTab);
          pane.container.parentDijit = registry.byId(pane.parentTab);
        }

        pane.container.id = json.id;
        pane.container.title = json.title;
        pane.container.type = dijit_types[json.type] ? dijit_types[json.type]: BorderContainer;
        console.log("Creating the panes and widgets");
        console.log("Received JSON: ");
        console.log(json);

        if (! dom.byId( pane.container.id ) ) {
          console.log("No Pane DOM created yet. Creating the same");
          console.log("Placing the DOM Node at: "  + 
                      pane.container.parentDomNode + 
                      " with an ID of " + 
                      pane.container.id 
                    );
          pane.container.domNode = domConstruct.create('div',
                                                       { id: pane.container.id },
                                                       pane.container.parentDomNode,
                                                       'last'
                                                      );
        }

        if (! registry.byId( pane.container.id ) ) {
          console.log("No Pane Dijit created yet. Creating the same");
          pane.container.dijit = new pane.container.type({ id: pane.container.id, 
                                                           closable: pane.container.closable, 
                                                           title: pane.container.title
                                                        });
          pane.container.dijit.startup();
          pane.container.parentDijit.addChild( pane.container.dijit );
          pane.container.parentDijit.resize();      
        }

        else{
          console.log( "No Pane Dijit exists. Selecting it." );        
          pane.container.parentDijit.selectChild( 
                registry.byId( pane.container.id ) 
          );
        }


        console.log("Building the widgets array ...");
        for ( var x=0; x< json.widgets.length; x++ ) {
          pane._widgetQueue.push({widget: json.widgets[x], parent: pane.container.id});
        }
        console.log("Created the widgets array");

        console.log("Starting to create Panes...");
        for ( var x=0; x< json.panes.length; x++ ){
          pane._createPane( json.panes[x], pane.container.id );
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

        pane.container.parentDijit.selectChild(pane.container.dijit);

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

                    if (! dom.byId(paneDomId) ){

                      if ( p.domType == 'img' ){
                        domConstruct.create('img',
                                            {id: paneDomId, 
                                             src: p.src},
                                            parentDomId,
                                          'last');
                      }
                      else {
                        domConstruct.create('div',
                                          {id: paneDomId},
                                          parentDomId,
                                        'last');
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

                    if ( ! registry.byId( paneDomId ) ){

                      if ( p.type == 'cp' ) { 
                        var pd = new paneType({id: paneDomId,
                                               title: paneTitle,
                                               region: paneRegion,
                                               closable: paneClosable,
                                               href: href,
                                               splitter: splitter,
                                               style: p.style ? p.style : ''
                                            },
                                            paneDomId );
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

                    console.log( "Creating Widgets with Args: ");                
                    console.log( widgetQ );
                    console.log( "This widget is of type: " + widgetQ.widget.type );

                    function createDom() {
                        if (! dom.byId(widgetQ.widget.id) ){
                          domConstruct.create('div',
                                              {id: widgetQ.widget.id},
                                              widgetQ.parent,
                                              'last');
                        }
                    }

                    require(
                      ['aushadha/tree/pane_tree_creator'],
                      function(paneTreeCreator){

                        createDom();

                        console.log("Creating Widget with title: " + widgetQ.widget.title );

                        if ( widgetQ.widget.hasOwnProperty('mainTabPane') ){
                          pane.mainTabPaneDomNode = widgetQ.widget.mainTabPane;
                        }

                        if ( widgetQ.widget.type == 'tree' ){

                          paneTreeCreator(widgetQ.widget.url, 
                                          widgetQ.widget.id, 
                                          widgetQ.widget.mainTabPane,
                                          widgetQ.widget.title
                                        );

                        }

                        else if ( widgetQ.widget.type == 'grid' ){
                            require(['aushadha/grid/generic_grid_setup',
                                    'aushadha/grid/grid_structures'],
                            function(genericGridSetup, gridStr){ 
                                console.log(genericGridSetup);
                                console.log(gridStr[widgetQ.widget.str]);
                                genericGridSetup.setupGrid(widgetQ.widget.url,
                                                          widgetQ.widget.id,
                                                          gridStr[widgetQ.widget.str],
                                                          widgetQ.widget.activateRowClick,
                                                          widgetQ.widget.title,
                                                          widgetQ.widget.storeToUse
                                );                                      
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
                            addButton.constructor({gridId: widgetQ.widget.id, 
                                                  label: widgetQ.widget.label,
                                                  title: widgetQ.widget.title,
                                                  url: widgetQ.widget.url
                            });
                        }

                        else if ( widgetQ.widget.type == 'something_else' ){

                        }

                      });
    }

  }

  return pane;

});