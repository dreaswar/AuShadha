function publishInfo(infoMessage){
  require(["dojo/ready","dojox/widget/Toaster"],
  function(ready){
    ready(function(){
        var info = new dojox.widget.Toaster({
            messageTopic: '/app/info',
            positionDirection: 'br-up',
            duration: 5000,
            type:'message',
            style:"opacity:0.85;"
        });

        window.setTimeout(function(){
            dojo.publish('/app/info', [infoMessage]);
        }, 100);
    });
  });
}

function publishError(errorMessage){
  require(["dojo/ready","dojo/query","dojo/dom-style","dojox/widget/Toaster"],
  function(ready, query, domStyle){
    ready(function(){
        var errors = new dojox.widget.Toaster({
            messageTopic: '/app/error',
            positionDirection: 'br-up',
            type:'error',
            duration: 5000,
            style:"opacity:0.85;"
        });

        dojo.publish('/app/error', [errorMessage]);

    });
  });
}