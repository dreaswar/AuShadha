require(

['dojo/dom','dojo/on','dijit/registry','dijit/Dialog','dijit/form/Button'],

function(dom,on,registry,Dialog,Button){
  var dialogButton = function(args){
     var btn = new Button({id: args.id, label: args.label});
     btn.onClick = function(){
                          new Dialog({href: args.url}).show();
     }
     btn.startup
  }

  return dialogButton;

});
~                                                                                                                                                                                   
~                                                                                                                                                                                   
~                                                                                                                                                                                   
~                                                              
