/*
Raise an Invalid Form Submission Dialog and return false
*/

function raiseInvalidFormSubmission() {
    require(["dijit/registry"], function (registry) {
        registry.byId("invalidFormSubmissionErrorDialog")
            .show();
        return false;
    });
    return false;
}


/*
Raise an Permission Denied Dialog and return false
*/

function raisePermissionDenied() {
    require(["dijit/registry"], function (registry) {
        registry.byId("permissionDeniedErrorDialog")
            .show();
        return false;
    });
    return false;
}
