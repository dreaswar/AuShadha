<div data-dojo-type = "dijit/form/Form" 
     id             = "newDemographicsAddOrEditForm" 
     data-dojo-id   = "newDemographicsAddOrEditForm"
     encType        = "multipart/form-data" 
     action         = "" 
     method         = "">

  <script type="dojo/on" data-dojo-event="submit">
 
    if( this.validate() ){

      require(["dijit/registry", 
               "dojo/request",
               "dojo/dom",
               "dojo/dom-form",
               "dojo/json",
               "dojo/_base/fx",
               "dojo/domReady!"
      ],

      function(registry, request, dom, domForm, JSON,fx){

          var url = "{{action}}";
          var form_data = domForm.toObject('newDemographicsAddOrEditForm');

          request(url,{method:"POST", data: form_data}).
          then( 

            function(json){

              var jsondata = JSON.parse(json);

              if (jsondata.success == true){

                if (jsondata.editUrl){

                  publishInfo(jsondata.error_message);
                  registry.byId("DEMOGRAPHICS_CENTER_BC_TOP_CP").set('href', jsondata.editUrl);

                }

                else{

                  publishInfo(jsondata.error_message);

                }

              }
            },

            function(json){

              var jsondata = JSON.parse(json);
              publishError(jsondata.error_message);

            },

            function(evt){

              publishError(evt);
              return false

            });

      return false
    });
    
      return false
    
    }

    else{
        raiseInvalidFormSubmission();
        return false
    }

  </script>


<table>
    <tr> <td> <label for="id_date_of_birth"> Birth Date</label> </td>
         <td> {{demographics_form.date_of_birth}}  </td>
    </tr>
    <tr>
        <td > <label for="id_socioeconomics"> Socioeconomics</label> </td>
        <td > {{demographics_form.socioeconomics}}
              <label for="id_education"> Education </label>
              {{demographics_form.education}}
        </td>
    </tr>
    <tr>
        <td > <label for="id_housing_condition"> Housing</label> </td>
        <td>  {{demographics_form.housing_conditions}} </td>
    </tr>
    <tr>
        <td > <label for="id_religion"> Religion</label> </td>
         <td> {{demographics_form.religion}}
              {{demographics_form.religion_notes}}</td>
    </tr>
    <tr>
        <td > <label for="id_race"> Race</label> </td>
        <td>  {{demographics_form.race}} </td>
    </tr>
    <tr>
        <td > <label for="id_religion"> Languages</label> </td>
        <td> {{demographics_form.languages_known}} </td>
    </tr>

</table>

    <button data-dojo-type = "dijit/form/Button" 
            data-dojo-props="iconClass: 'dijitEditorIcon dijitEditorIconSave'"
            type           = "submit" 
            name           = "{{button_label}}Button" 
            value          = "{{button_label}}"
    >
      {{button_label}}
    </button>

  {% if canDel %}

  <button data-dojo-type  = "dijit/form/Button" 
		  data-dojo-props = "iconClass: 'dijitEditorIcon dijitEditorIconDelete'"
          type            = "button"
          name            = "delDemographics"
          id              = "delDemographicsBtn"
   >

    Delete

    <script type="dojo/on" data-dojo-event="click" >

      var confirmDialog = confirm('This will delete the Demographics.. Are you Sure ? ')

      if (confirmDialog == true){

        require(["dojo/request", 
                 "dojo/json", 
                 "dojo/dom", 
                 "dijit/registry"
                 ], 

        function(request, JSON, dom, registry){

        request("{{delUrl}}",{method: "GET"}).
        then(

            function(json){
              var jsondata = JSON.parse(json);

              if(jsondata.success == true){

                publishInfo(jsondata.error_message);
                registry.byId("DEMOGRAPHICS_CENTER_BC_TOP_CP").set('href', jsondata.addUrl);
              }

              else{
                publishError(jsondata.error_message);
              }

            },

            function(json){
              var jsondata = JSON.parse(json);
              publishError(jsondata.error_message);
            }
          );

        });

      }

      else{
        return false
      }
  </script>

  </button>

{% endif %}