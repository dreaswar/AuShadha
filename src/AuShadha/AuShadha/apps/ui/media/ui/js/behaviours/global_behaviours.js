define(['dojo/dom',
       'dojo/dom-style',
       'dojo/dom-construct',
       'dojo/behavior',
       'dojo/query',
       'dojo/ready',
       'dojo/domReady!'],

function(dom,
         domStyle,
         domConstruct,
         behavior,
         query,
         ready){

    genericFormBehaviour = function(){
        var FormBehaviour = {
             "#id_patient_detail":{
                found:   function(el){ domStyle.set(el, 'display','none')}
             },
             "label[for=id_patient_detail]":{
                found:   function(el){ domStyle.set(el, 'display','none')}
             },
             "#id_admission_detail":{
                found:   function(el){ domStyle.set(el, 'display','none')}
             },
             "label[for=id_admission_detail]":{
                found:   function(el){ domStyle.set(el, 'display','none')}
             },
             "#id_visit_detail":{
                found:   function(el){ domStyle.set(el, 'display','none')}
             },
             "label[for=id_visit_detail]":{
                found:   function(el){ domStyle.set(el, 'display','none')}
             },
             "#id_phy_exam_detail":{
                found:   function(el){ domStyle.set(el, 'display','none')}
             },
             "label[for=id_phy_exam_detail]":{
                found:   function(el){ domStyle.set(el, 'display','none')}
             },
            "#id_consult_nature":{
                found:   function(el){ domStyle.set(el, 'display','none')}
             },
             "label[for=id_consult_nature]":{
                found:   function(el){ domStyle.set(el, 'display','none')}
             },
             "span[class= helptext]":{
                found:   function(el){
                                   domStyle.set(el, 'font-size','8px');
                                   domStyle.set(el, 'color','RoyalBlue');
                                   domStyle.set(el, 'font-style','italic');
                         }
             }
        }
        behaviour.add(FormBehaviour)
        behaviour.apply()
    }
});