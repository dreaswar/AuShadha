require(["dojo/parser",'dojo/ready','dojo/domReady!'],
function(parser,ready){
  ready( 
    function() { parser.parse(); } 
  );
});

/*

Handle Login..
*/

function handleLogin() {
    require(["dojo/request",
               "dojo/dom",
               "dojo/json",
               "dijit/registry",
               "dijit/Dialog",
               "dojo/dom-form",
               "dojo/domReady!"
      ],
        function (request, dom, JSON, registry, Dialog, domForm) {
            var dialog = registry.byId("loginErrorDialog");
            var loginDialog = registry.byId('loginDialog');
            request("/AuShadha/login/", {
                data: domForm.toObject("loginForm"),
                method: "POST",
                handleAs: "text"
            })
                .
            then(function (json) {
                    var jsondata = JSON.parse(json)
                    if (jsondata.success == true) {
                        if (loginDialog) {
                            loginDialog.hide();
                        }
                        window.location.href = jsondata.redirect_to;
                    } else {
                        var content = jsondata.error_message;
                        dialog.set('title', "ERROR! ");
                        dialog.set('content', content);
                        dialog.show();
                    }
                },
                function (json) {
                    var jsondata = JSON.parse(json)
                    dialog.set('title', "ERROR! ");
                    dialog.set('content', jsondata.error_message);
                    dialog.show();
                },
                function (evt) {
                    console.log("Login Handler executed successfully...");
                }
            );
            return false;
        });
}