// The module loader for AuShadha scripts
define(['dojo/dom',
        'dojo/dom-construct',
        'dojo/dom-style',
        'dojo/dom-class',
        'dojo/on',
        'dojo/json',
        'dojo/_base/array',
        'dijit/registry',
        'dijit/layout/BorderContainer',
        'dojox/layout/ContentPane',
        'dijit/layout/TabContainer',
        "dojo/parser",
        "dojo/request",
        "dojo/json",
       'dojo/domReady!'
    ],
    function (
        dom,
        domConstruct,
        domStyle,
        domClass,
        on,
        JSON,
        array,
        registry,
        BorderContainer,
        ContentPane,
        TabContainer,
        parser,
        request,
        JSON
       ){

      var pane = {

        panes: [],
        parentTab: '',

        constructor: function( appObj ) {

              pane.parentTab = appObj.parentTab;
              appPaneCreator( appObj );
              var numChildren = pane.parentTab.getChildren().length;
              var lastChild = pane.parentTab.getChildren()[numChildren-1];
              pane.parentTab.selectChild(lastChild);

        },

        destroyPane: function(){
          for( var x = 0; x < pane.panes.length; x++ ) {
            pane.parentTab.removeChild( pane.panes[x] );
            registry.byId( pane.panes[x].domNode ).destroyRecursive();
          }
        }

      }

      function appPaneCreator( appObj ) {

        var title = appObj.title;
        var url = appObj.url; 
        var domId = appObj.domId;
        var d = dom.byId(domId);
        var p = registry.byId(domId);

        if ( !p ) {

          if ( !d ){

            var paneDom = domConstruct.create('div',
                                                {id: domId},
                                                pane.parentTab.domNode,
                                                'last'
                                            );

          }

          var cp = new ContentPane({title: title, 
                                    closable:true,
                                    id:domId,
                                    class:"subTabContainer",
                                    href : url,
                                    executeScripts: true,
                                    scriptHasHooks: true
                                   },
                                   domId
                                  );
          cp.startup();
          pane.parentTab.addChild( cp );

//           var reloadPane  = domConstruct.create('div',
//                                     {id : domId + "_reloadPaneIcon", 
//                                      style : "float:right; ",
//                                      innerHTML : window.ICONS.RELOAD_PANE
//                                     },
//                                     domId,
//                                     0
//                                 );
// 
//           console.log("Created RELOAD_IMG");
//           console.log(reloadPane.innerHTML);

        }

        pane.panes.push(p);

    }

    return pane.constructor ;

});