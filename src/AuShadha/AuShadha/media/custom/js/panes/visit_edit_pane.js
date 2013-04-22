define(['dojo/dom'           ,
        'dojo/dom-construct' ,
        'dojo/dom-style'     ,
        'dijit/registry'     ,

        'dijit/layout/BorderContainer',
        'dojox/layout/ContentPane'    ,
        'dijit/layout/TabContainer'   ,

        'aushadha/panes/visit_pane'   ,
        'aushadha/tree/visit_tree'
       ],
  function(dom             ,
           domConstruct    ,
           domStyle        ,
           registry        ,
           BorderContainer ,
           TabContainer    ,
           ContentPane     ,
           VISITPANE       
  ){

    var visitEditPane = {

      visitPaneContentArea : registry.byId('visitPaneContentArea'),

      initialized          : function(){
                              if(registry.byId('visitEditPaneTabContainer')){
                                return true
                              }
                              else{
                                return false;
                              }
      },

      doms                 : function(){
                              if(!dom.byId('visitEditPaneTabContainer')){
                                domConstruct.create('div',
                                                    {id: 'visitEditPaneTabContainer'},
                                                    'visitPaneContentArea',
                                                    'first');
                                  domConstruct.create('div',
                                                      {id: 'visitEditPane'},
                                                      'visitEditPaneTabContainer',
                                                      'first');
                              }
      },

      dijits               : function(html){
                                var visitEditPaneTabContainer = new TabContainer({id         : 'visitEditPaneTabContainer', 
                                                                                 tabStrip    : true, 
                                                                                 tabPosition : 'top'},
                                                                                 'visitEditPaneTabContainer'
                                                                                );
                                var mainContentArea = registry.byId('visitPaneContentArea');
                                mainContentArea.addChild(visitEditPaneTabContainer);
                                var visitEditPane             = new ContentPane({id      : 'visitEditPane',
                                                                                title    : "Edit Visit"},
                                                                                'visitEditPane');
                                console.log(visitEditPane);
                                visitEditPane.startup();
                                visitEditPaneTabContainer.addChild(visitEditPane);                                
                                visitEditPaneTabContainer.startup();
//                                 visitEditPane.startup();
//                                 this.visitPaneContentArea.startup();
      },

      constructor          : function(html){
                                if (!this.initialized()){
                                  this.doms();
                                  this.dijits(html);
                                  this.initialized();
                                }
                                else{
                                  this.destroyPane();
                                }
      },

      destroyPane          : function(){
                                if(registry.byId('visitEditPaneTabContainer')){
                                  var visitEditPaneTabContainer = registry.byId('visitEditPaneTabContainer');
                                  if( registry.byId('visitEditPane')){
                                    visitEditPaneTabContainer.removeChild('visitEditPane');
                                  }
                                  visitEditPaneTabContainer.destroyRecursive();
                                }
                                this.initialized();
                                this.constructor();
      }

    }

   return visitEditPane;

});