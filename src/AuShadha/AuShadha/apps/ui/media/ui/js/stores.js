/* Defines the Stores for use throught the AuShadha applicaion. 
 * Defined in stores.js
 * returns AuShadha Store variable
 * 
*/


define([
        "aushadha/complaints",
        "aushadha/durations",
        "aushadha/patient_list",
       
        "dojo/dom",
        "dojo/parser",
        "dojo/store/JsonRest",
        "dojox/data/JsonRestStore",
        "dojo/data/ObjectStore",
        "dojo/behavior",
        "dojo/store/Memory",

        "dojo/data/ItemFileWriteStore",
        "dojox/data/QueryReadStore",
        "dojo/store/Observable",
        "dojo/domReady!"
      ],
      function(
               COMPLAINTS,
               COMPLAINT_DURATIONS,
               PATIENT_LIST,

               dom, 
               parser,   
               JsonRest, 
               JsonRestStore, 
               ObjectStore , 
               behaviour, 
               Memory
              ){
  
  var aushadhaStore = {

    complaints           : new Memory({data:COMPLAINTS}),           // console.log(complaintsStore);

    complaintDurations   : new Memory({data:COMPLAINT_DURATIONS}),  //console.log(complaintDurationsStore);

    patientList          : new Memory({data:PATIENT_LIST})          //console.log(patientListStore);

  }
  
  console.log(aushadhaStore);

  return aushadhaStore;

});