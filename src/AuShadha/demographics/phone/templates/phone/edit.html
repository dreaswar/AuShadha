{% if user and user.is_authenticated %}
<div data-dojo-type = "dijit/form/Form" 
     id             = "newphoneEditForm" 
     data-dojo-id   = "newphoneEditForm"
     encType        = "multipart/form-data" 
     action         = "" 
     method         = "">

  <script type="dojo/method" 
          data-dojo-event="onSubmit"
  >

    if( this.validate() ){
      require(["dijit/registry",
               "dojo/domReady!"
      ],
       function(registry){
         //	{% if perms.phone.change_phone %}
          editItem("{{phone_obj.urls.edit}}","newphoneEditForm");
         // {% else %}
          registry.byId("permissionDeniedErrorDialog").show();
         // {%endif %}
         return false;
   	   }
 		  );
     return false;
    }
    else{
     raiseInvalidFormSubmission();
     return false;
    }

  </script>

    <table>
      {{phone_form}}
    </table>

   {%if perms.phone.change_phone %}
      <button data-dojo-type = "dijit/form/Button" 
              data-dojo-props="iconClass: 'dijitEditorIcon dijitEditorIconSave'"
              type           = "submit" 
              name           = "editButton" 
              value          = "Edit">
        Edit
      </button>
   {% endif %}

   {% if perms.phone.delete_phone %}
      <button data-dojo-type  = "dijit/form/Button" 
              data-dojo-props = "iconClass: 'dijitEditorIcon dijitEditorIconDelete'"    
              type            = "button"
              name            = "delphone"
              id              = "delphoneBtn">

         Delete

        <script type="dojo/method" 
                data-dojo-event="onClick" 
                data-dojo-args="evt"
        >
            //	{% if perms.phone.delete_phone %}
                delItem("{{phone_obj.urls.del}}");
            // {% else %}
            registry.byId("permissionDeniedErrorDialog").show();
            // {%endif %}
        </script>

      </button>

    {% endif %}
</div>
{% endif %}
