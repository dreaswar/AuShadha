require(
        [
         'dojo/dom'          ,
         'dijit/registry'    ,
         'dojo/dom-style'    ,
         'dojo/dom-construct',
         'dojo/dom-attr'     ,
         'dojo/dom-geometry' ,
         'dojo/_base/window' ,
         'dojo/query'
        ],

function(dom          ,
         registry     , 
         domStyle     , 
         domConstruct , 
         domAttr      , 
         domGeom      , 
         win){

var overLay = function(){
                if(dom.byId('overlay') ){
                  domConstruct.destroy('overlay');
                }
                domConstruct.create('div', 
                                    {id: "overlay"}, 
                                    win.body(),
                                    'first');
                 domConstruct.create('div', 
                                    {class: "dijitContentPaneLoading", 
                                     id: 'insideOverlay'}, 
                                    'overlay',
                                    'first');
                domStyle.set('overlay',{ background: 'white', 
                                         height: '100%',
                                         width : '100%',
                                         zIndex  : '100000',
                                         opacity : 0.2
                                        });
                domStyle.set( 'insideOverlay',
                                        { position: 'relative',
                                         top : '30%', 
                                         left: '30%',
                                         height: '100%',
                                         width : '100%'
                                        });
}

overLay();        
         
});