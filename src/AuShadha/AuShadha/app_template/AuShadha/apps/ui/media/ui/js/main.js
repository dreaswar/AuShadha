// The module loader for AuShadha scripts
define([
        'dojo/dom',
        'dojo/on',
        'dijit/registry',
        'dojo/parser',
        'dojo/ready',
        'dojo/dom-style',
        'dojo/request',
        'dojo/json',

        'aushadha/stores',
        'aushadha/behaviours/global_behaviours',
        "aushadha/grid/generic_grid_setup",
        'aushadha/event_binders/main',
        'aushadha/panes/main',

        'aushadha/notifications',

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

          auStore,
          auBehaviours,
          auGridSetup,
          auEventBinders,
          auPanes,
          auNotifications) {

        console.log("Returning Main.js");

        var auMain = {
            auStore: auStore,
            auGridSetup: auGridSetup,
            auBehaviours: auBehaviours,
            auEventBinders: auEventBinders,
            auPanes: auPanes,
            auNotifications: auNotifications
        }

        return auMain;

});