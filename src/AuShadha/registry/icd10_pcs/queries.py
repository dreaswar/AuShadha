########################################################################
# Project: AuShadha
# Documentation: Queries the ICD10PCS db and store values as constants
# License: GNU GPL Version3
# Author: Dr. Easwar T.R
# Date: 05-04-2014
########################################################################

""" Queries the ICD10PCS db and store values as constants """


from .models import RootXML, PcsTable, PcsRow, Axis, Label, Title, Definition

QUERIED = False

all_tables = PcsTable.objects.all()
section_list = []
body_system_list = []
operation_list  = []
 

section_mapper = {}
body_system_mapper = {}
operation_mapper = {}

    

def generate_all_tables(): 
  global all_tables
  global section_list
  global body_system_list
  global operation_list
  section_temp_list = []

  for table_obj in all_tables:
  
    section_label = table_obj.get_section_name()
    section_code = table_obj.get_section()[0].code
    body_system_label = table_obj.get_body_system_name()
    operation_label = table_obj.get_operation_name()

    if section_label not in section_temp_list:
       section_temp_list.append(section_label)
       section_list.append({'name': section_label,'code': section_code} )

    if body_system_label and body_system_label not in body_system_list:
       body_system_list.append(body_system_label)   

    if operation_label and operation_label not in operation_list:
       operation_list.append(operation_label)


def generate_table_wise_axis_names():

    global section_mapper
    global all_tables

    for table in all_tables:
       s = table.get_section_name()
       bs = table.get_body_system()
       bs_name = table.get_body_system_name()
       op = table.get_operation()
       op_name = table.get_operation_name()
       if section_mapper.get(s):
          if not bs_name in section_mapper[s].get('body_system_names'):
              section_mapper[s]['body_system'].append(bs)
              section_mapper[s]['body_system_names'].append(bs_name)
          if not op_name in section_mapper[s].get('operation_names'):
              section_mapper[s]['operation'].append(op) 
              section_mapper[s]['operation_names'].append(op_name)
       else:
          section_mapper[s] = {'body_system':[bs],
                               'body_system_names': [bs_name],
                               'operation':[op],
                               'operation_names': [op_name]
                              }   


def generate_body_system_operation_mapper():

    global body_system_mapper
    global all_tables

    def build_op_list():
          for o in op:
            if o.fk.pcsTable_fk.get_section_name() == sec:
                if not o.pk in body_system_mapper[sec][bs_name].get('operation_id'):
                    body_system_mapper[sec][bs_name]['operation'].append(o) 
                    body_system_mapper[sec][bs_name]['operation_id'].append(o.pk)

    for table in all_tables:
       sec = table.get_section_name()
       bs = table.get_body_system()
       bs_name = table.get_body_system_name()
       op = table.get_operation()
 
       if not body_system_mapper.get(sec):
          body_system_mapper[sec] = {bs_name:{}}      

       if body_system_mapper[sec].get(bs_name):
          build_op_list()
       else:
          body_system_mapper[sec][bs_name] = {'operation':[],'operation_id': []}   
          build_op_list()


def return_tables_items_by_section_name(section_name):

    """ Returns collection of tables for a section name """

    table_list = []
    body_system_list = []
    operation_list = []

    for table in all_tables:
       if table.get_section_name() == section_name:
           table_list.append(table)
       if table.get_body_system_name() not in body_system_list:
           body_system_list.append(table.get_body_system_name())
       if table.get_operation_name() not in operation_list:
           operation_list.append(table.get_operation_name())

    return {'tables': table_list, 
            'body_systems': body_system_list,
            'operations': operation_list
           }



def return_tables_by_axis_name(axis_name,axis_type='section'):

    """ Returns collection of tables for a Axis  name """

    table_list = []
    mapper = {'section': 'get_section_name', 
              'body_system': 'get_body_system_name', 
              'operation': 'get_operation_name'
             }
    for table in all_tables:
       if getattr(table, mapper[axis_type],None)() == axis_name:
           table_list.append(table)
    return table_list



# This is an interim arranagement to test the code
# This function can be replaced with a JSON from its own output. 
# This JSON file can be loaded at runtime and accessed by the views

def main():

  """
      Checks the QUERIED value and updates all the dictionary and lists.
      This can then be accessed by the views. 
      However, this will rerun every time the server is restarted. 
      This is not optimal and should be replaced
  """

  print("Starting to query and aggregate ICD10PCS codes. This has not been done before. This will take time.")
  global QUERIED
  if not QUERIED:
     generate_all_tables()
     generate_table_wise_axis_names()       
     generate_body_system_operation_mapper()
     QUERIED = True

main()
 
