/*
    Contains the Logic of eventing in Patient Search Form Partly.
    Some of it is implemented in the HTML declaratively.
    Triggered when the patient search text is entered
    A separate trigger is present in search/patient.html
    for handling the click event of the Filter button
*/

define (["dojox/timing",
        "dojo/dom",
        "dojo/dom-style",
        "dojo/dom-construct",
        "dijit/registry",
        "dojo/date/locale",
        "dojo/ready",
        'dijit/form/FilteringSelect',
        "dojo/store/JsonRest",
//         "aushadha/grid_setup_alt.js",
        'aushadha/panes/main',
        'aushadha/panes/event_controller',
        "dojo/domReady!"
],
function(timing,
         dom,
         domStyle,
         domConstruct,
         registry,
         dateLocale,
         ready, 
         FilteringSelect,
         JsonRest,
         auPaneMain,
         auPaneEventController
        ){

    var headerPane= {
            headerPane        : function(){
                                  registry.byId("header_area");
            },

            headerPaneWidgets : function(){ 
                                    return ( registry.findWidgets('header_area') ) 
              
            },

            headerTimer : function(){
                            console.log("Starting script headerTimer.js");
                            ready(function(){
                              var t = new timing.Timer(60000);
                              var fmt = "MMMM d yyyy  - hh:mm ";
                              function dateFormat(d, f){
                                return dojo.date.locale.format(d, {selector: "date", datePattern: f})
                              }
                              t.onTick = function(){
                                var timeNow = new Date();
                                var timeBox = dom.byId("timeBox").innerHTML = dateFormat(timeNow, fmt);
                              }
                              t.onStart = function(){
                                var timeNow = new Date();
                                var timeBox = dom.byId("timeBox").innerHTML = dateFormat(timeNow, fmt);
                              }
                              t.start();
                            });
            },
            searchWidget : function(){
                            var widgetStore = new JsonRest({target: PAT_SEARCH_JSON_URL});

                            /*
                            domStyle.set('filteringSelectPatSearchSmall',
                                         {width      : '250px',
                                          height     : '18px',
                                          margin     : 'none',
                                          padding    : 'none',
                                          position   : 'relative',
                                          top        : '-3.0em',
                                          marginLeft : '10px'
                            });
                            */

                            var searchBox = new FilteringSelect({regExp        : '[a-zA-Z0-9 -]+',
                                                                required       : true,
                                                                invalidMessage : 'No Results',
                                                                store          : widgetStore,
                                                                searchAttr     : 'name',
                                                                labelAttr      : 'label',
                                                                labelType      : 'html',
                                                                autoComplete   : false,
                                                                placeHolder    : 'Patient\'s Name',
                                                                hasDownArrow   : false,
                                                                onChange       : function(e){ 
                                                                                    auPaneEventController.onPatientChoice(this);
                                                                                }
                                                                },
                                                                'filteringSelectPatSearchSmall');

                            searchBox.startup();
            }
            
    }
    headerPane.headerTimer();
    headerPane.searchWidget();
    
    return headerPane;
 });                      