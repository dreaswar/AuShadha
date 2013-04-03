define(

function(){
        var search_pane_event_callbacks={
        // Event for autofiltering the Patient Grid on Searchbox entry
        // May link with panes/search_pane events
        patSearchOnKeyUp:  function (e){
                                console.log(e.target);
                                var search_field   = patSearchForFilteringSelect.get('value');
                                var txt            = filterPatGridTextBox.get('value');
                                var search_obj     = { search_field : search_field , search_for : txt };
                                if( !filterPatGridTextBox.get('value') || !patSearchForFilteringSelect.get('value') ){
                                  search_obj.search_for   = "*"
                                  search_obj.search_field = "id"
                                }
                                registry.byId('patient_grid').filter(search_obj, true);
                            },

        // Events for changing the searchbox entries
        // Should go into panes/search_pane events
        patSearchForFilteringSelectOnChange:function (newVal){
                                                if(newVal){
                                                  console.log(newVal);
                                                  if(newVal == 'full_name'){
                                                    dom.byId("searchLinker").innerHTML = "contains..";
                                                    filterPatGridTextBox.focus();
                                                  }
                                                  else if(newVal == 'id'){
                                                    dom.byId("searchLinker").innerHTML = "equal to";
                                                    filterPatGridTextBox.focus();
                                                  }
                                                  else{
                                                    dom.byId("searchLinker").innerHTML = "starts with..";
                                                    filterPatGridTextBox.focus();
                                                  }
                                                }
                                                else{
                                                  console.log("No Selection Supplied.. Enforcing Full Name selection..")
                                                  patSearchForFilteringSelect.set('displayedValue', 'Full Name');
                                                  dom.byId("searchLinker").innerHTML = "contains..";
                                                  filterPatGridTextBox.focus();
                                                }
                                          }
    }
});