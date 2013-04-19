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

      initialized          : false,

      doms                 : function(){
                              if(!dom.byId('visitEditPaneTabContainer')){
                                domConstruct.create('div',
                                                    {id: 'visitEditPaneTabContainer'},
                                                    'visitPaneContentArea',
                                                    0);
                                  domConstruct.create('div',
                                                      {id: 'visitEditPane'},
                                                      'visitEditPaneTabContainer',
                                                      0);
                              }
      },

      dijits               : function(html){
                                var visitEditPaneTabContainer = new TabContainer({id         : 'visitEditPaneTabContainer', 
                                                                                 tabStrip    : true, 
                                                                                 tabPosition : 'top'},
                                                                                 'visitEditPaneTabContainer'
                                                                                );
                                this.visitPaneContentArea.addChild(visitEditPaneTabContainer);
                                var visitEditPane             = new ContentPane({id      : 'visitEditPane',
                                                                                title    : 'Edit Visit',
                                                                                content  : html,
                                                                                closable : true},
                                                                                'visitEditPane');
                                console.log(visitEditPane);
                                visitEditPaneTabContainer.addChild(visitEditPane);
                                visitEditPaneTabContainer.startup();
//                                 this.visitPaneContentArea.startup();
      },

      constructor          : function(html){
                                if (!this.initialized){
                                  this.doms();
                                  this.dijits(html);
                                  this.initialized = true;
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
                                this.initialized = false;
                                this.constructor();
      }

    }

   return visitEditPane;

});