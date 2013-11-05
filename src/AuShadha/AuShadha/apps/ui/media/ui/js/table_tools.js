function tableTools(obj /* {tableId    : String | domNode,
                            totalForms : String | Int, 
                            totalFormId: String | domNode,
                            emptyForm  : HTML Fragment,
                            snippets   : [HTML Fragment list], 
                            icons      : {add: 'addIcon', 
                                          remove: 'removeIcon'
                                        }
                            }
                        */) {
  

  var TOTAL_FORMS = obj.totalForms;
  var TOTAL_FORM_AUTO_ID: obj.totalFormId;
  var TABLE_ID = obj.tableId;

  var USED_PREFIX=[];
  var AVAILABLE_PREFIX=[];
  for(var i=0; i < parseInt(TOTAL_FORMS); i++){
    USED_PREFIX.push(i);
  }

  var addIcon     = obj.icons.remove;      
  var removeIcon  = obj.icons.add;      
  var ACTION_CELL = "<td class='actionCell'>"+removeIcon + addIcon+"</td></tr>";  
  // escapejs filtered emptyForm HTML snippet
  var emptyForm  = obj.emptyForm; 
//var emptyVisitComplaintForm  = emptyVisitComplaintForm.replace(/__prefix__/g, TOTAL_FORMS);

  var snippetRow = '';
  for (var i=0; i<obj.snippets.length; i++){
    var _str = '<tr><td>'+obj.snippet[i]+'<td>';
    _str += "<td class='actionCell'>"+removeIcon + addIcon+"</td></tr>";
    // Create TABLE CELLS with passed snippets filtered with escapejs
    snippetRow += _str; 
  }

  var TABLE = require(["dojo/dom",
                "dojo/request",
                "dijit/registry"  ,
                "dojo/json"       ,
                "dojo/dom-form"   ,
                "dijit/Dialog"    ,
                'dojo/dom-class',
                'dojo/dom-style',
                'dojo/dom',
                'dojo/query',
                'dojo/dom-attr',
                'dojo/dom-construct',
                'dojo/_base/lang',
                "dojo/on",
                'dojo/parser',
                'dojo/NodeList-traverse',
                'dojo/NodeList-data'
        ],
        function(dom, 
                request, 
                registry, 
                JSON, 
                domForm, 
                Dialog, 
                domClass,
                domStyle,
                dom,
                query,
                domAttr,
                domConstruct,
                lang,
                on,
                parser){

              var Tools={

                getAllRows: function (node /*String | domNode */){
                              //           console.log(node);
                                    var n = query("#"+node)[0];
                              //           console.log(n);
                                    if (n.tagName == 'TABLE'){
                                      var allRows = query(n).children('tbody').children('tr');
                                    }else if(n.tagName != "TABLE"){
                                      var allRows = query(n).parents('table').children('tbody').children('tr');
                                    }else{
                                      console.log("Query fetched nothing");
                                      return;
                                    }
                                    console.log("Returning All Rows of Table from getAllRows Function");
                                    console.log(allRows);
                                    return allRows;
                            },

                getNumRows: function (table_id/*String | domNode */){
                              var allRows = getAllRows(table_id);
                              return allRows.length;
                            },

                getLastRow: function (table_id/*String | domNode */){
                          //           console.log(table_id);
                                var allRows = getAllRows(table_id);
                          //           console.log(allRows.length)
                                if (allRows.length>0){
                                  console.log("Returning Last row...");
                                  console.log( query(allRows[allRows.length-1]) );
                                  return query(allRows[allRows.length-1]);
                                }else{
                                  console.log("No Rows !. Cannot get the last row");                            
                                  return null;
                                }
                              },

                getFirstRow: function (table_id/*String | domNode */){
                                var allRows = getAllRows(table_id);
                                if (allRows.length>0){
                                  return query(allRows[0]);
                                }else{
                                  console.log("No Rows !. Cannot get the first row");
                                  return null;
                                }
                              },

                getRowIndex: function (row/*query obj */){
                              if(getAllRows >0){
                                var allRows = getAllRows();
                                try{
                                  return allRows.indexOf(row[0]);
                                }catch(err){
                                  console.log(err.message);
                                  return
                                }
                              }else{
                                console.log("No Rows to the number for !");
                              }
                            },

                getRowFromTable: function (table_id /* String | domNode */,r /*String*/){
                              var _r = parseInt(r);
                              console.log("Received request for Table Row No. " + r + " in Table id: " + table_id);
                              var _row_to_return = query("#"+table_id).children('tbody').children('tr')[_r-1];
                              console.log("Returning Row with number: " + _r);
                              console.log(_row_to_return);
                              return _row_to_return;
                            },

                _getLastElem: function (l){
                              if (l.length>0){
                                l.sort();
                                var _l = l.length;
                                var i = _l-1;
                                var e = l[i];
                                return parseInt(e);
                              }else{
                                return null;
                              }
                          },


                returnUnusedPrefix: function (){
                                AVAILABLE_PREFIX.sort();            
                                USED_PREFIX.sort();                

                                if(AVAILABLE_PREFIX.length >= 1 ){

                                  var _last_elem = _getLastElem(AVAILABLE_PREFIX);

                                  if (USED_PREFIX.indexOf(_last_elem) == -1 ){
                                      console.log("USED_PREFIX does not have the element");
                                      console.log("LAST ELEMENT OF USED_PREFIX" + USED_PREFIX.indexOf(_last_elem).toString());
                                      AVAILABLE_PREFIX.pop();
                                      AVAILABLE_PREFIX.sort();
                                      USED_PREFIX.push(_last_elem);
                                      USED_PREFIX.sort();
                                      console.log("USED_PREFIX is" + USED_PREFIX.toString());
                                      console.log("AVAILABLE_PREFIX is" + AVAILABLE_PREFIX.toString());
                                      return _last_elem;
                                  }else{
                                    console.log("USED_PREFIX has the element");
                                    console.log("LAST ELEMENT OF USED_PREFIX" + USED_PREFIX.indexOf(_last_elem).toString());
                                    console.log("USED_PREFIX is" + USED_PREFIX.toString());
                                    console.log("AVAILABLE_PREFIX is" + AVAILABLE_PREFIX.toString());
                                    // FIXME May be an edge case.. but still...
                                  }
                                  

                                }else{
                                  var _last_elem = _getLastElem(USED_PREFIX);
                                  var _new_elem = parseInt(_last_elem) +1;
                                  USED_PREFIX.push(_new_elem);
                                  USED_PREFIX.sort();
                                  console.log("USED_PREFIX is" + USED_PREFIX.toString());
                                  console.log("AVAILABLE_PREFIX is" + AVAILABLE_PREFIX.toString());
                                  return _new_elem;
                                }

                              },


                rehashPrefixes: function (node){
                                var n_id= domAttr.get(node.domNode,'id');
                                var _id = parseInt(n_id.match(/\d+/g)[0]);
                                var _available_ = AVAILABLE_PREFIX.indexOf(_id);
                                var _used_ = USED_PREFIX.indexOf(_id);          

                                if(_available_ == -1){          
                                  if(_used_ != -1){
                                    USED_PREFIX.splice(_used_,1);
                                    AVAILABLE_PREFIX.push(_id);
                                    console.log("USED_PREFIX is" + USED_PREFIX.toString());
                                    console.log("AVAILABLE_PREFIX is" + AVAILABLE_PREFIX.toString());
                                  }else{
                                    console.log("PREFIX_ERROR!! PREFIXES CANNOT BE PRESENT IN BOTH LISTS");
                                    console.log("USED_PREFIX is" + USED_PREFIX.toString());
                                    console.log("AVAILABLE_PREFIX is" + AVAILABLE_PREFIX.toString());
                                  }
                                }else{
                                  AVAILABLE_PREFIX.splice(_available_,1);
                                  USED_PREFIX.push(_id);
                                  console.log("USED_PREFIX is" + USED_PREFIX.toString());
                                  console.log("AVAILABLE_PREFIX is" + AVAILABLE_PREFIX.toString());
                                }
                                AVAILABLE_PREFIX.sort();
                                USED_PREFIX.sort();

                              },


                lastButOneRowActionCellStyling: function (){
                                                var _t_id=TABLE_ID;
                                        //             var lastRow = getLastRow(table_id);
                                                var _rn= parseInt(getNumRows(_t_id));
                                                console.log("Querying for Row with Number " + (_rn-1) + " in Table with ID: " + _t_id);
                                                if (_rn>=1){
                                                  var _lbr = getRowFromTable(_t_id, _rn-1);
                                        //               console.log(_lbr);
                                                  var _aIcon = query(_lbr).children('td.actionCell').children('span.showNextComplaint')[0];
                                                  var _rIcon = query(_lbr).children('td.actionCell').children('span.removeThisComplaint')[0];
                                                  domStyle.set(_aIcon, {'display':'none'});
                                                  domStyle.set(_rIcon,{'display':'table-cell'});
                                                }else{
                                                  return;
                                                }
                                            },

                lastRowActionCellStyling: function (){
                                            var table_id=TABLE_ID;
                                            var lastRow = getLastRow(table_id);
                                            var addIcon = lastRow.children('td.actionCell').children('span.showNextComplaint')[0];
                                            var removeIcon = lastRow.children('td.actionCell').children('span.removeThisComplaint')[0];
                                            domStyle.set(addIcon, {'display':'table-cell'});
                                            domStyle.set(removeIcon,{'display':'table-cell'});
                                        },

                setTotalFormInputNumber: function (){
                                          var table_id=TABLE_ID;
                                          var numberOfRows = getNumRows(table_id);
                                          TOTAL_FORMS = numberOfRows;
                                          domAttr.set(TOTAL_FORM_AUTO_ID,{'value':TOTAL_FORMS});
                                        },

                incrementTotalFormInput: function (){
                                            TOTAL_FORMS ++;
                                            domAttr.set(TOTAL_FORM_AUTO_ID,{'value':TOTAL_FORMS});
                                        },

                decrementTotalFormInput: function (){
                                            TOTAL_FORMS --;
                                            domAttr.set(TOTAL_FORM_AUTO_ID,{'value':TOTAL_FORMS});
                                        },


                placeAndDijitiseRows: function (){
                                        var prefix = this.returnUnusedPrefix();

                                        var HTMLToInsert = snippetRow.replace(/__prefix__/g, prefix);

                                        var rowInserted = domConstruct.place(HTMLToInsert,query("#" + TABLE_ID +" tbody")[0] );
                                        parser.parse(rowInserted);
                                        var addIcon = query(rowInserted).
                                                          children('td.actionCell').
                                                          children('span.showNextComplaint')[0];
                                        var removeIcon = query(rowInserted).
                                                          children('td.actionCell').
                                                          children('span.removeThisComplaint')[0];

                                        on(addIcon,
                                           'click',
                                           this.onAddMoreComplaintsClick
                                        );
                                        on(removeIcon,
                                           'click',
                                           function(){ 
                                              this.onRemoveComplaintClick(removeIcon);
                                            }
                                        );
                                        this.setTotalFormInputNumber();
                                      },

                onAddMoreComplaintsClick: function (){
                                          this.placeAndDijitiseRows();
                                          this.lastButOneRowActionCellStyling();
                                          this.lastRowActionCellStyling();
                                    },

                rollBackRows: function (r){
                                      var table_id = TABLE_ID;

                                      if(this.getNumRows(table_id) >1){
                                        registry.
                                            findWidgets(r).
                                              forEach(function(n,i){
                                                        if (i==0){ this.rehashPrefixes(n); }
                                                        n.destroyRecursive(false);
                                                      });

                                        domConstruct.destroy(r);
                                      }

                                      if(this.getNumRows(table_id) >1){
                                        this.lastButOneRowActionCellStyling();
                                      }
                                      this.lastRowActionCellStyling();
                                      this.setTotalFormInputNumber();
                                    },

                onRemoveComplaintClick: function (evt){

                                      if (confirm("This will delete the complaint.. Proceed ?")){
                                        var closestRow    = query(evt).closest('tr');
                                        var rowToDelete   = closestRow[0];
                                        var delBtn        = closestRow.
                                                              children('td.actionCell').
                                                              children('span.removeThisComplaint')[0];
                                        var parentTable = closestRow.parents('table');
                                        var urlToCall   = domAttr.get(delBtn,'data-url');

                                        if(urlToCall !== 'null'){
                                          console.log("Requesting delete of the complaint");
                                          request(urlToCall).then(
                                          function(json){
                                            var jsondata = JSON.parse(json);
                                            if(jsondata.success == true){
                                              publishInfo("Successfully Deleted Complaint");
                                              this.rollBackRows(rowToDelete);
                                            }else{
                                              publishError("ERROR! "+ jsondata.error_message);
                                            }
                                          },
                                          function(){
                                            publishError("ERROR! Server Error");
                                          }
                                          );
                                        }else{
                                          console.log("Deleting the Complaint forms");
                                          this.rollBackRows(rowToDelete);
                                          console.log("Destroyed Empty forms");
                                        }

                                      }
                                      console.log("CONFIRM_DIALOG_CLOSED");
                                    },

              bindAddMoreComplaintsClick: function (){
                                        query('.showNextComplaint').forEach(
                                        function(node){
                                          on(node,'click', this.onAddMoreComplaintsClick);
                                        });
                                      },

              bindRemoveComplaintsClick: function (){
                                          query('.removeThisComplaint').forEach(
                                          function(node){
                                              on(node,'click',function(evt){ this.onRemoveComplaintClick(evt.target);});
                                          });
                                        }
              }

              Tools.bindAddMoreComplaintsClick();
              Tools.bindRemoveComplaintsClick();
              return Tools;
            });

  return TABLE;
}