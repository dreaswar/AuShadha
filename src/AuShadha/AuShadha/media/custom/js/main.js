// The module loader for AuShadha scripts

define(['aushadha/script_alt',
        'aushadha/stores'
       ],
function(script_alt, aushadhaStores){
  console.log("Returning Main.js");

  return {aushadhaScript : script_alt,
          aushadhaStores : aushadhaStores
  };
});