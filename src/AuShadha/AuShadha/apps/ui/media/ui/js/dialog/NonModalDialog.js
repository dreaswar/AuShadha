define("aushadha/dialog/NonModalDialog", 

       ["dijit/Dialog",  
        "dijit/DialogUnderlay", 
        "dojo/_base/declare"
       ], 

       function(Dialog, DialogUnderlay, declare){

        var NonModalDialog = declare("aushadha.dialog.NonModalDialog", 
                                     [Dialog], 
                                     {postCreate : function(){
                                                    this.inherited(arguments);
                                                    require(['dijit/registry',
                                                    'dojo/dom',
                                                    'dojo/on',
                                                    'dojo/dom-style',
                                                    'dojo/dom-attr'
                                                    ],
                                                    function(registry,
                                                            dom,
                                                            on,
                                                            domStyle,
                                                            domAttr){
                                                      var thisDialogId =  domAttr.get(this.domNode,'id');
                                                      try{
                                                        domStyle.set(dom.byId(thisDialogId+"_underlay"),
                                                                      {opacity : '0',
                                                                      zIndex  : '-1',
                                                                      display : "none"
                                                                      }
                                                        );
                                                      }catch(err){
                                                          console.log(err.message);
                                                      }
                                                      console.log("Popup Styling complete");
                                                    });
                                      }
        });
        return NonModalDialog;
});
