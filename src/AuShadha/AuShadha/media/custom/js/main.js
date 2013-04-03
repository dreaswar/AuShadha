// The module loader for AuShadha scripts

define(['dojo/dom',
        'dojo/on',
        'dijit/registry',
        'dojo/parser',
        'dojo/ready',
        
        'aushadha/stores',
        'aushadha/behaviours/global_behaviours',
        "aushadha/grid/grid_setup",
        'aushadha/event_binders/main',

        'notifications',
        'key_bindings',
        
        'dojo/domReady!'
       ],
function(dom,
         on,
         registry,
         parser,
         ready,

         auStore, 
         auBehaviours,
         auGridSetup,
         auEventBinders,
         auNotifications,
         auKeyBindings
        ){
  
    console.log("Returning Main.js");

    console.log("Calling setupPatientGrid");
      auGridSetup.setupPatientGrid();
    console.log("setupPatientGrid Returned");
    
    console.log("Dojo code has loaded");
    
    console.log(auEventBinders);

    var auMain= {auStore         : auStore,
            auGridSetup     : auGridSetup,
            auBehaviours    : auBehaviours,
            auEventBinders  : auEventBinders,
            auNotifications : auNotifications,
            auKeyBindings   : auKeyBindings
    };
    return auMain;
});