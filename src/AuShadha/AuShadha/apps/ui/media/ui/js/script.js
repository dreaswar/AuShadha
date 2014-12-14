/* The Main AuShadha script that runs and sets everything up
 * Basically this 
 *   1) loads the required dojo and aushadha modules
 *   2) fades away the loader
 *   3) creates INSTALLED_APPS and UI globals
 *   4) creates a wireframe UI with regions and blocks
 *   5) uses the search module to fill it with Search functionality
 * 
*/

  require([
          "dojo/dom",
          "dojo/_base/xhr",
          "dojox/grid/DataGrid",
          "dojo/store/JsonRest",
          "dojox/data/JsonRestStore",
          "dojo/data/ObjectStore",
          "dojo/on",
          "dijit/registry",
          "dijit/Dialog",
          "dojo/ready",
          "dojo/_base/array",
          "dojo/dom-construct",
          "dojo/dom-style",
          "dojox/layout/ContentPane",
          "dojo/behavior",
          "dojo/store/Memory",
          "dojo/dom-geometry",
          "dojo/request",
          "dojo/_base/fx",
          'dojo/parser',

          'aushadha/main',
          'aushadha/panes/create',

          "dojo/_base/connect",
          "dijit/TitlePane",
          "dijit/layout/TabContainer",
          "dijit/layout/BorderContainer",
          "dijit/layout/SplitContainer",
          "dijit/Editor",
          "dijit/form/Form",
          "dijit/form/Button",
          "dijit/form/TextBox",
          "dijit/form/ValidationTextBox",
          "dijit/form/Textarea",
          "dijit/form/SimpleTextarea",
          "dijit/form/DateTextBox",
          "dijit/form/TimeTextBox",
          "dijit/form/NumberTextBox",
          "dijit/form/NumberSpinner",
          "dijit/form/Select",
          "dijit/form/MultiSelect",
          "dijit/form/FilteringSelect",
          "dojox/form/Manager",
          "dojox/validate/web",
          "dijit/Tooltip",
          "dijit/Tree",
          "dojo/store/Observable",
          "dijit/dijit",
          "dojox/widget/Toaster",
          "dijit/Menu",
          "dijit/MenuBar",
          "dijit/PopupMenuBarItem",
          "dijit/DropDownMenu",
          "dijit/MenuItem",
          "dojo/data/ItemFileWriteStore",
          "dojox/data/QueryReadStore",
          "dojo/domReady!"
  ],

  function (dom,
      xhr,
      DataGrid,
      JsonRest,
      JsonRestStore,
      ObjectStore,
      on,
      registry,
      Dialog,
      ready,
      array,
      domConstruct,
      domStyle,
      ContentPane,
      behaviour,
      Memory,
      domGeom,
      request,
      fx,
      parser,

      auMain,
      auCreatePane
  ) {

        // Define Variables to be used later in the app..
        ready( function () {

          console.log("Starting script script.js");

          /* Defines a function to get all the installed applications in AuShadha
            * This JSON is then added as a INSTALLED_APPS global
            * The json.UI returned is added as a UI global
            * The UI is an attempt to make this process cleaner. 
            * Currently it does nothing important
            * Most of the heavy lifting is done by the INSTALLED_APPS variable
            * Once these are set auCreatePane() is called
          */

          function getInstalledApps() {

            request( URL_installed_apps /* Variable from urls.js */ ).

              then(
                function( json ){

                  var jsondata = JSON.parse(json);

                  if ( jsondata.success == true ){

                    window.INSTALLED_APPS = jsondata.installed_apps; // window.INSTALLED_APPS global is set
                    window.UI = jsondata.UI;                         // window.UI global is set

                    auCreatePane();                                  // This module loads the UI with Search functionality
                                                                     // This module was initially created for loading many applications at once
                                                                     // Now this only loads the Search module.

                                                                     // Lot of code is commented out / left as stubs here.
                                                                     // This has not been replaced intentionally as user may want to load more
                                                                     //   modules at load time along with Search
                  }
                  else{
                    publishError(jsondata.error_message);
                  }
                },

                function( json ){
                  var jsondata = JSON.parse(json);
                  publishError(jsondata.error_message);
                },

                function(evt){
                  publishError(evt);
                }
              );
          }


            /* 
             * Defines the fadeAwayLoader function for fading loader away
             * Check the DOM is ready to be parsed
             * Hide the loader indicator and fade it away.
             * Call the URL_render_aushadha_ui_pane and set up the UI
            */
            var fadeAwayLoader = fx.fadeOut({
                node: dom.byId('aushadhaLoaderIndicator'),
                duration: 3300
            });

            // Binds the event hide it
            on( fadeAwayLoader,
                "End",
                function () {
                    domStyle.set(dom.byId('aushadhaLoaderIndicator'), {display: 'none'} );
                }, 
                true
            );

            /* Actual work starts
             * The UI wireframe is loaded --> This is a basic wireframe UI with no functionality. Basic blocks and regions are defined here
             * getInstalledApps is run    --> Loads the Search UI on top of the wireframe UI from auCreatePane() function
             * Timer is created           --> Creates the timer widget in headerPane
             * Loader is faded away       --> Fades away and hides the loding animation, logo and messages
            */
            require(['dojo/request',
              'dojo/dom',
              'dojo/parser',
              'dojo/ready',
              'dojo/json',
              'dijit/registry',

              'aushadha/under_construction/app_container_creator',
              'aushadha/timer',

              'dojo/domReady!'
              ],

            function( request,
                      dom,
                      parser,
                      ready,
                      JSON,
                      registry,
                      appContainerCreator, 
                      timer ){

              ready(

              function(){

                  request( URL_render_aushadha_ui_pane /* Variable from urls.js */).
                  then(
                    function(json){

                      var jsondata = JSON.parse(json);

                      var pane = jsondata.pane;                 // The pane variable returned contains the JSON to set up search UI

                      appContainerCreator.constructor( pane );  // A basic UI is set up. This is just a wireframe UI
                                                                //   without Search module or other widgets built using JSON returned
                                                                //   by the ui/dijit_widget/pane/render_aushadha_ui_pane which 
                                                                //   uses the YAML markup in turn.

                                                                // Search UI will be loaded by the getInstalledApps function
                                                                //   when it runs the auCreatePane inside it

                      console.log("Getting The Installed Apps from script.js");

                      getInstalledApps();                       // Additional INSTALLED_APPS are obtained with this function and globals set

                      fadeAwayLoader.play();                    // After all the lifting is over and UI ready, the loader is faded away

                      console.log("Finished running the Animations and Fading it..");

                      parser.parse('tooltipsAndDialogs');       // The tooltips_and_dialogs.html is parsed

                      timer();                                  // Timer widget is set at header pane

                    },

                    function(json){
                      var jsondata = JSON.parse(json);           // In case of error say Sorry !
                      alert("ERROR! UI could not be loaded");
                      console.error(jsondata.error_message);
                    }

                  );
                }
              );

            });

    });

});