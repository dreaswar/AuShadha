// Notification area events
// Sets up the notification area with events, popups, drop downs etc..
// This can be used to set notification area icons event binders
 
define([
        'dojo/dom',
        'dojo/on',
        'dijit/registry',
        'dojo/parser',
        'dojo/ready',
        'dojo/dom-style',
        'dojo/request',
        'dojo/json',
        'dojo/dom-construct',
        'dijit/Tooltip',
        'dijit/Dialog',
        'dijit/TooltipDialog',
        'dijit/popup',
        'dojo/query',
        'dojo/dom-attr',
        'dojo/dom-class',
        'dojo/dom-style',
        'dojo/NodeList-traverse',
        'dojo/NodeList-data',
        'dojo/domReady!'
       ],

function (dom,
          on,
          registry,
          parser,
          ready,
          domStyle,
          request,
          JSON,
          domConstruct,
          Tooltip,
          Dialog,
          TooltipDialog,
          Popup,
          query,
          domAttr,
          domClass,
          domStyle
        ) {

   (function () {
       request(URL_get_reference_apps /*GLOBAL from url.js*/).
       then(
         function(html){
            window.REFERENCE_APPS =  html;
          }
        );
    })();

    function createTooltipDialog() {

        if (registry.byId('appsIcon_TooltipDialog') ) {
            registry.byId('appsIcon_TooltipDialog').destroyRecursive();
        }

        var myTooltipDialog = new TooltipDialog({
            id: 'appsIcon_TooltipDialog',
            style: "width: 300px;",
            content: window.REFERENCE_APPS,
            onMouseLeave: function(){
                             Popup.close(myTooltipDialog);
                          }
       });

       function onReferenceAppClick(e){
        console.log(e);
        if ( domClass.contains(e.target,'referenceApp') ) {
           e.preventDefault();
           var _url = domAttr.get(e.target, 'data-url');  
           require(['aushadha/under_construction/pane_and_widget_creator'],
           function(paneAndWidgetCreator){
                 request( _url ).
                 then(
                     function( json ){
                           var jsondata = JSON.parse(json);
                           paneAndWidgetCreator.constructor( jsondata.pane );
                           },
                     function(json){
                                    var jsondata = JSON.parse(json);
                                    publishError(jsondata.error_message);
                     }
                 );
            });
        }  
       }

       myTooltipDialog.on('click',onReferenceAppClick);      
       return myTooltipDialog 
    }

    on(dom.byId('appsIcon'), 'click', function(){
        Popup.open({
            popup: createTooltipDialog(),
            around: dom.byId('appsIcon')
        });
    });
    
});
