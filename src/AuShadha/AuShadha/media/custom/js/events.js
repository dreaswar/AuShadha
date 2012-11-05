    /* 
       Contains the Logic of eventing in Patient Search Form Partly. 
       Some of it is implemented in the HTML declaratively.
       Triggered when the patient search text is entered 
       A separate trigger is present in search/patient.html
       for handling the click event of the Filter button
    */

    function patSearchOnKeyUp(e){
      console.log(e.target);
      var search_field   = patSearchForFilteringSelect.get('value');
      var txt            = filterPatGridTextBox.get('value');
      var search_obj     = { search_field : search_field , search_for : txt };
      if( !filterPatGridTextBox.get('value') || !patSearchForFilteringSelect.get('value') ){
        search_obj.search_for   = "*"
        search_obj.search_field = "id"
      }
      grid.filter(search_obj, true);
    }

    function patFilteringSearchOnKeyUp(e){
      require(["dijit/registry","dojo/dom","dojo/dom-style","dojo/dom-construct"], 
      function(registry, dom, domStyle, domConstruct){
/*
        var search_field   = patSearchForFilteringSelect.get('value');
        var txt            = filteringSelectPatSearch.get('value');
        var search_obj     = { search_field : search_field , search_for : txt };
        if( !filteringSelectPatSearch.get('value') || !patSearchForFilteringSelect.get('value') ){
          search_obj.search_for   = "*"
          search_obj.search_field = "full_name"
        }
        console.log("You searched for " + search_obj.search_for + search_obj.search_field);
        console.log( e.store.get( e.get('value') ) );
*/
        e.store.get(e.get('value')).then(
          function(item /*returned item*/){
            console.log(item)
//            console.log(contactStore);
            domStyle.set('selected_patient_info',{"display":"","padding":"0px","margin":"0px"});
            var addData = item.addData;
            var selectedPatientContent = addData.full_name + "-" + addData.age +"-" + addData.sex +"(" +addData.patient_hospital_id +")"
            registry.byId('selected_patient_info').set('content', selectedPatientContent);
            var demographicsUrl = "/AuShadha/pat/demographics/add/"+addData.id+"/";
            registry.byId("demographics_add_or_edit_form").set('href', demographicsUrl);
          }
        );
      });
//      patSearchForJsonRestStore.query("?search_for="+search_obj.search_field +"&search_field="+search_obj.search_field)
    }

    function patSearchForFilteringSelectOnChange(newVal){
      if(newVal){
        console.log(newVal);
        if(newVal == 'full_name'){
          dojo.byId("searchLinker").innerHTML = "contains..";
          filterPatGridTextBox.focus();
        }
        else if(newVal == 'id'){
          dojo.byId("searchLinker").innerHTML = "equal to";
          filterPatGridTextBox.focus();
        }
        else{
          dojo.byId("searchLinker").innerHTML = "starts with..";
          filterPatGridTextBox.focus();
        }
      }
      else{
        console.log("No Selection Supplied.. Enforcing Full Name selection..")
        patSearchForFilteringSelect.set('displayedValue', 'Full Name');
        dojo.byId("searchLinker").innerHTML = "contains..";
        filterPatGridTextBox.focus();
      }
    }


