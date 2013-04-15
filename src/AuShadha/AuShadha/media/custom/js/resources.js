define(
  ['dojo/_base/declare'],
  function(declare){

    var auResources = {
      auIcons:{
          MALE           : '{{STATIC_URL}}images/male.png',
          FEMALE         : '{{STATIC_URL}}images/female.png',
          NOTIFICATION   : '{{STATIC_URL}}images/notification.png'
      },
      auUrls: {
          
      }
    }

  return declare('auResources', function(){
    return auResources;
  });

});