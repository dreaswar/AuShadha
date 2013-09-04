/*
    Contains the Logic of eventing in Patient Search Form Partly.
    Some of it is implemented in the HTML declaratively.
    Triggered when the patient search text is entered
    A separate trigger is present in search/patient.html
    for handling the click event of the Filter button
*/

function patSearchOnKeyUp(e) {
    console.log(e.target);
    var search_field = patSearchForFilteringSelect.get('value');
    var txt = filterPatGridTextBox.get('value');
    var search_obj = {
        search_field: search_field,
        search_for: txt
    };
    if (!filterPatGridTextBox.get('value') || !patSearchForFilteringSelect.get(
        'value')) {
        search_obj.search_for = "*"
        search_obj.search_field = "id"
    }
    grid.filter(search_obj, true);
}


function patSearchForFilteringSelectOnChange(newVal) {
    if (newVal) {
        console.log(newVal);
        if (newVal == 'full_name') {
            dojo.byId("searchLinker")
                .innerHTML = "contains..";
            filterPatGridTextBox.focus();
        } else if (newVal == 'id') {
            dojo.byId("searchLinker")
                .innerHTML = "equal to";
            filterPatGridTextBox.focus();
        } else {
            dojo.byId("searchLinker")
                .innerHTML = "starts with..";
            filterPatGridTextBox.focus();
        }
    } else {
        console.log("No Selection Supplied.. Enforcing Full Name selection..")
        patSearchForFilteringSelect.set('displayedValue', 'Full Name');
        dojo.byId("searchLinker")
            .innerHTML = "contains..";
        filterPatGridTextBox.focus();
    }
}

}