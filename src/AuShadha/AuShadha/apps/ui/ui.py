################################################################################
# Project     : AuShadha
# Description : Provides the UI app for AuShadha. The Core UI and its elements. 
# License     : GNU-GPL Version 3, see LICENSE.txt for details
# Author      : Dr. Easwar T.R
# Date        : 15-10-2013
################################################################################



import importlib

from AuShadha.settings import INSTALLED_APPS
from AuShadha.settings import APP_ROOT_URL
from AuShadha.core.views.dijit_tree import DijitTree, DijitTreeNode


###################### EXPERIMENTAL CODE #######################################

class UIClass(object):
  
  """ 

    The parent UIClass that all UIClass objects inherit from. 

    This is meant to pass the metadata for UI along with the ModelClass it is registered for

    This metadata is passed to UI along with AuShadhaUI object instance 

  """
  


class Containers:

  dijit_class_name = ['BorderContainer',
                      'TabContainer',
                      'ContentPane',
                      'StackContainer',
                      'Dialog',
                      'Tooltip'
                      ]

  available_positions = ['leading','top','center','trailing','bottom']

  def __init__(self):
    self.container_layout ={}

  def create_main_container(self):
    self.container_layout['BorderContainer']  = {}
    return self.container_layout


class Tree:
  url = ''
  structure_node = [DijitTree] # for Tree Structure as instance of DijitTree

class Grid: 
  url = ''
  structure = ''

class Widgets:
  available_widgets = [Containers,Tree, Grid]

class Layout:
  columns = {'column': [Containers,]}



################################################################################






class AlreadyRegisteredException(Exception):

  def __call__(self):
    return Exception("AlreadyRegisteredException")

  def __repr__(self):
    return str("AlreadyRegisteredException")



class NotRegisteredException(Exception):

  def __call__(self):
    return Exception("NotRegisteredException")

  def __repr__(self):
    return  str("NotRegisteredException")



class RoleRegistry(object):
  
  """ 
    Registers accepted Roles on UI. Things like PatientRegistration, Admission, OPD Visits, Medical History 

    Basically any function a module is supposed to perform. 

    The UI will allow registration of one module for each function even if many that perform the same function are
    installed. 
    
    In case a module that is already set is overridden, a check will be made for database consistency and then a module will be 
    chosen. Supposed there are two modules for History : H_1 and H_2
    
    In a situation where H_1 and H_2 both seek registration, 
    
    If any other module; Admission module for example depends on H_1, then it will be registered in preference. 
    
    In case there is a clash with some other module an Exception will be raised and registration prevented.
    
    UI_INSTALLATION_STATE variable will be set to False
  
  """
  def __init__(self):
    self.roles = [
                  'PatientRegistration',
                  'Admission',
                  'OpdVisits',
                  'MedicalHistory',
                  'SurgicalHistory',
                  'FamilyHistory',
                  'SocialHistory',
                  'Medication',
                  'Allergy',
                  'LabInvestigations',
                  'ImagingStudies',
                  'Demographics',
                  'Contact',
                  'Phone',
                  'Guardian',
                  'EmailAndFax',
                  'Immunisation'
                ]

  def __call__(self):
      return self.roles

  def register_role(self, role):
    if not role in self.roles:
      self.roles.append(role.capitalize())
    else:
      raise AlreadyRegisteredException("AlreadyRegisteredException")

  def unregister_role(self, role):
    if not role in self.roles:
      raise NotRegisteredException("NotRegisteredException")
    else:
      self.roles.remove(role.capitalize())

  def update_role(self, role):
    if not role in self.roles:
      raise NotRegisteredException("NotRegisteredException")
    else:
      self.roles.remove(role.capitalize())





class ModuleRegistry(object):
  
  """ 
    Aggregates all the installed_modules on settings.py and checks the __init__.py for imports / registration 
    
  """
  
  def __init__(self):
    self.modules = []
    self.installed_modules = INSTALLED_APPS
    self.registered_modules = []

    for module in INSTALLED_APPS:
      try:
        module = importlib.import_module(module)
      except(ImportError) as ex:
        raise ImportError(ex)
      
      if not module in self.modules:
        self.modules.append(module.__name__)
  
  def __call__(self):
      return self.modules





class AuShadhaUI(object):
  
  """
    The UI Object which will help registration of the elements of UI and installed modules
  """
  
 
  def __init__(self):

    self.UI_INSTALLATION_STATE  = False  
    self.registered_roles = RoleRegistry()
    self.registered_modules = ModuleRegistry()
    self.registry = {}

  def __call__(self):
    return self.registry
  
  def register(self, role,module):
    """ Registers a module with the UI for a particular role. """
    if role in self.registered_roles():
      if module not in self.registry.values():
        self.registry[role] = module
        if module not in self.registered_modules():
          self.registered_modules().append(module)
      else:
        for k, v in self.registry:
          if v == role:
            key = k
            message  = "This module is already registered for a role:: ", self.registry[key]
            raise AlreadyRegisteredException(message)
          else:
            continue
    else:
      raise NotRegisteredException("Not a acceptable role")


  def check_registry(self):
    """ Checks the registry and raises an AlreadyRegisteredException if the module is registered already """
    pass
  
  def update_module(self, module_name, module_role):
    """ Update a particular module and its role """
    pass
  
  def delete_module(self, module_name):
    """ Registers a module with the UI for a particular role. """
    pass
  
  def get_module_for_role(self, role):
    """ Gets a Module registered for a particular role. """
    pass


#Creates an instance of the AuShadhaUI
ui = AuShadhaUI()