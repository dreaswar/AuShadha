define([
  'dojo/on',
  'dojo/dom',
  'dojo/dom-style',
  'dojo/dom-construct',
  'dojo/dom-geometry',
  'dojo/ready',
  'dijit/registry',
  'dojo/request',
  'dojo/json',

  'aushadha/panes/header_pane',
  'aushadha/panes/patient_pane',
  'aushadha/panes/admission_pane',
  'aushadha/panes/visit_pane',
  'aushadha/panes/patient_search_pane',
  'aushadha/panes/event_controller'

  ],
  function(on,
           dom,
           domStyle,
           domConstruct,
           domGeom,
           ready,
           registry,
           request,
           JSON,
           
           auHeaderPane,
           auPatientPane,
           auAdmissionPane,
           auVisitPane,
           auSearchPane,
           auPaneEventController
          ){

    return {auHeaderPane          : auHeaderPane,
            auPatientPane         : auPatientPane,
            auAdmissionPane       : auAdmissionPane,
            auVisitPane           : auVisitPane,
            auSearchPane          : auSearchPane,
            auPaneEventController : auPaneEventController
    }

});  
 
