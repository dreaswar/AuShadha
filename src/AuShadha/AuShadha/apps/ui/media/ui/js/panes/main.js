define([
  'dojo/on',
  'dojo/dom',
  'dojo/dom-style',
  'dojo/dom-construct',
  'dojo/dom-geometry',
  'dojo/ready',
  'dijit/registry',
  'dojo/request',
  'dojo/json',

  'aushadha/panes/event_controller'

  ],
  function(on,
           dom,
           domStyle,
           domConstruct,
           domGeom,
           ready,
           registry,
           request,
           JSON,

           auPaneEventController
          ){

    return {auPaneEventController : auPaneEventController}

});  
 
