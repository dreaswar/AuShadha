// The module loader for AuShadha scripts
define(['dojo/dom',
        'dojo/on',
        'dijit/registry',
        'dojo/parser',
        'dojo/ready',
        'dojo/dom-style',

        'aushadha/stores',
        'aushadha/behaviours/global_behaviours',
        "aushadha/grid/grid_setup",
        'aushadha/event_binders/main',
        'aushadha/panes/main',

        'notifications',

        'dojo/domReady!'
       ],
    function (dom,
        on,
        registry,
        parser,
        ready,
        domStyle,

        auStore,
        auBehaviours,
        auGridSetup,
        auEventBinders,
        auPanes,
        auNotifications
    ) {

        console.log("Returning Main.js");

        console.log("Calling setupPatientGrid");
        auGridSetup.setupPatientGrid();
        console.log("setupPatientGrid Returned");

        var auMain = {
            auStore: auStore,
            auGridSetup: auGridSetup,
            auBehaviours: auBehaviours,
            auEventBinders: auEventBinders,
            auPanes: auPanes,
            auNotifications: auNotifications
        };

        return auMain;
    });