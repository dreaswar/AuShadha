define(['dojo/dom',
        'dojo/on',
        'dijit/registry',
        'dijit/Dialog',
        'dijit/form/Button',
        'dojo/dom-construct',
       ],

   function(dom,on,registry,Dialog,Button,domConstruct){

       var setupDialogButton = function(args){

//           console.log(args);
//           debugger;
           var btnDomId = args[0].id+"_button";
           if ( registry.byId(btnDomId) ){
              registry.byId(btnDomId).destroyRecursive();
           }
           if( !dom.byId(btnDomId) ){
                domConstruct.create('button',
                                    { id: btnDomId,
                                      type:'button',
                                      label: args[0].label
                                    },
                                    args[0].id,
                                    0);
                console.log("Created the Button DOM Node with ID: "+ btnDomId); 
           }
           
           var btn = new Button({onClick: function(){
                                          new Dialog({href: args[0].url}).show();
                                         },
                                 label: args[0].label,
                                 id: btnDomId
                                },
                                btnDomId);
           btn.startup();
           console.log("Calling Button's startup");
           console.log(btn);
       }

       console.log(setupDialogButton);

//       debugger;   

       return setupDialogButton;

});
