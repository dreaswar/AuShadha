define(["dojo/dom",
       'dijit/form/Button',
       'dijit/registry',
       'dojo/request',
       'dojo/_base/array',
       'dojo/dom-construct',
       'dojo/dom-attr',
       'dojo/dom-class',
       'dijit/Dialog'
       ],

function(dom,
        Button,
        registry,
        request,
        array,
        domConstruct,
        domAttr,
        domClass,
        Dialog){
  
       var addButton = function(obj){

                            var args= obj;

                            var b = new Button({
                                        label       : args.label,
                                        title       : args.title,
                                        iconClass   : "dijitIconNewTask",
                                        onClick: function(){
                                                            request(args.url).
                                                            then(

                                                              function(html){
                                                                console.log("Calling URL:: " + args.url);
                                                                window.CHOSEN_GRID = args.gridId;

                                                                var dialog = registry.byId("editPatientDialog");
                                                                dialog.set('title',args.title);
                                                                dialog.set('content',html);
                                                                dialog.show();
                                                              },

                                                              function(json){
                                                                publishError(json.error_message);
                                                              }

                                                            );
                                                  }
                                        },
                                        domConstruct.create('button',
                                                            {type : "button",id: args.gridId+"_button"},
                                                            args.gridId,
                                                            "before")
                            );

                            return b;

      }

      return {
        constructor: function(obj){
                        return addButton(obj);
                     }
      }
});