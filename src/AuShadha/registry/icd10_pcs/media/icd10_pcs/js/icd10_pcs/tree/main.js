require(['dojo/dom',
         'dojo/on',
         'dojo/request',
         'dojo/json',
         'dojo/dom-construct',
         'dojo/dom-style',
         'dojo/dom-class',
         'dojo/dom-attr',
         'dojo/ready',
         'dojo/parser',
         'dijit/registry',
         'aushadha/tree/pane_tree_creator',
         'dojo/domReady!'
        ],

function(dom,
         on,
         request,
         JSON,
         domConstruct, 
         domStyle, 
         domClass, 
         domAttr, 
         ready, 
         parser, 
         registry,
         paneTreeCreator){


    var icd10tree =  paneTreeCreator(args.url, args.id,args.mainTabPane,args.title );
    icd10tree.tree.onDbClick = onTreeDblClick;
    function onTreeDblClick(){

        alert("Hello. You just clicked on the Tree !!. This was supposed to do something useful\nHowever, that something is under construction ");
    }



});
