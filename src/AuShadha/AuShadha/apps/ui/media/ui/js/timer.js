/*
    Contains the Logic of eventing in Patient Search Form Partly.
    Some of it is implemented in the HTML declaratively.
    Triggered when the patient search text is entered
    A separate trigger is present in search/patient.html
    for handling the click event of the Filter button
*/
define(["dojox/timing",
        "dojo/dom",
        "dojo/dom-style",
        "dojo/dom-construct",
        "dijit/registry",
        "dojo/date/locale",
        "dojo/ready",

        'dijit/form/FilteringSelect',
        "dojo/store/JsonRest",


        "dojo/domReady!"
],
    function (timing,
        dom,
        domStyle,
        domConstruct,
        registry,
        dateLocale,
        ready,

        FilteringSelect,
        JsonRest
    ) {

          var timer =  function () {
                            console.log("Starting script headerTimer.js");
                            ready(function () {
                                var t = new timing.Timer(60000);
                                var fmt = "MMMM d yyyy  - hh:mm ";

                                function dateFormat(d, f) {
                                    return dojo.date.locale.format(d, {
                                        selector: "date",
                                        datePattern: f
                                    })
                                }
                                t.onTick = function () {
                                    var timeNow = new Date();
                                    var timeBox = dom.byId("timeBox")
                                        .innerHTML = dateFormat(timeNow, fmt);
                                }
                                t.onStart = function () {
                                    var timeNow = new Date();
                                    var timeBox = dom.byId("timeBox")
                                        .innerHTML = dateFormat(timeNow, fmt);
                                }
                                t.start();
                            });
                        };

        return timer;

    });