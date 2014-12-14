################################################################################
# Project     : AuShadha
# Description : Constructing a Dijit Tree  
# Author      : Dr. Easwar T.R
# Date        : 25-09-2013
# License     : GNU-GPL Version 3 , See AuShadha/LICENSE.txt
################################################################################

"""
  This module and its classes used to generated DijitTree widgets

  This has now been partly replaced with PyYAML based markup and parsing
    to generate the JSON for the same. Part of the code is still used to construct 
    the tree using YAML

"""

import json 
#from django.core.serializers.json import DjangoJSONEncoder


class DijitTreeNode(object):

  """
    Class Based representation of a Tree Node

    Tree Node instances can be added to a Tree Instance with the add_child_node method

    __init__ takes dictionary with compulsary attrs of 'id','name', and 'type'

    These can be changed by subclassing the node / changing the self.basic_node_attrs

    Extra attributes can always be added. There is no restriction

    Child nodes can be added by using the add_child_node method. This takes the same 
        attrs as the DijitTreeNode class and checks for repetition of 'id' attribute. 
        DuplicateIDError is raised if 'id' is repeated. 

    Child node can be removed / edited / added as per requirement. 

  """

  def __init__(self,attrs):

    self.basic_node_attrs = ['name','type','id']
    self.extra_node_attrs = ['len','addUrl','children']
    self.id_registry={}

    if self.check_node_attr(attrs):
      self.node = attrs
      for k,v in attrs.iteritems():
        if k == 'id' and not self.id_registry.has_key(v):
          self.id_registry[v] = self.node
    else:
      raise Exception("InvalidInstantiationAttributes")

  def __setitem__(self,key,value):
    if self.node:
        old_val = self.__getitem__(key)
        self.node[key] = value
        if key =='id':
          self.id_registry.pop(old_val)
          self.id_registry[value] = self.node
    else:
      raise Exception("Node has not been set")

  
  def __getitem__(self,index):
    if self.node:
      try:
        return self.node[index]
      except KeyError:
        raise KeyError
  
  def __unicode__(self):
    return unicode(self.node)

  def __repr__(self):
    if self.node:
      return str(self.node)
    else:
      return "__repr__ function returning the self.node attribute"

  def __call__(self):
    return self.node

  def to_json(self):
    return json.dumps(self.node)

  #def set(self,key,value):
    #return self.__setitem__(key,value)

  #def get(self,index):
    #return self.__getitem__(index)

  def get_item_by_id(self,node_id):
    return self.id_registry.get(node_id)

  def check_node_attr(self, attrs):
    for attr in self.basic_node_attrs:
      if attrs.has_key(attr):
        continue
      else:
        return False
    return True

  def is_id_unique(self,attrs):
    id_val = attrs['id']
    if self.id_registry.has_key(id_val):
      raise Exception("DuplicateIDError: "+ id_val+'. Registry already has following keys: '+str(self.id_registry.keys()) )
    else:
      if self.node.has_key('children'):
        children = self.node['children']
        if children:
          for items in children:
            if items['id'] == id_val:
              raise Exception("DuplicateIDError")
            else:
              continue
      return True

  def add_child_node(self,attrs):
    if self.check_node_attr(attrs) and self.is_id_unique(attrs):
      if not self.node.has_key('children'):
        self.node['children'] = []
      self.node['children'].append(attrs.node)
    else:
      raise AttributeError





class DijitTree(object):

  """
    The DijitTree Class which generates the Tree.

    Takes parameters of 'identifier' and 'label' which should usually default to
    'id' and 'name'. These are sane defaults. 

    As of now it is assumed that 'id' attribute is unique and checks for duplicate 'id'
      whenever a branch is added / child node is added. DuplicateIDError is raised when 'id' 
      clashes

    A tree instance can add branches with DijitTreeNode instances using add_child_node method. 
  
  """
  
  def __init__(self,attrs = None):

    self.basic_tree_attrs = ['identifier','label']
    self.basic_branch_attrs = ['id','name','type']
    self.extra_branch_attrs = ['addUrl','children','len']
    self.id_registry=[]

    if not attrs:
      attrs = {'identifier':'id','label':'name','items':[]}

    if self.check_for_basic_attrs(attrs):
      self.identifier= attrs['identifier']
      self.label = attrs['label']
      if attrs.has_key('items'):
        self.items = attrs['items']
        if self.items:
          self.build_id_registry()
      else:
        self.items = []
        print "Initialised an empty tree"

      self.node = {'identifier':self.identifier,'label':self.label,'items':self.items}

  def check_for_basic_attrs(self,attrs):
    for attr in self.basic_tree_attrs:
      if attr in attrs:
        print "Checking for attribute: ", attr
        continue
      else:
        raise Exception("Basic Attributes Not Supplied while creating a tree")
    return True

  def check_for_duplicates(self,branch_id):
    if branch_id not in self.id_registry:
      return True
    else:
      raise Exception("DuplicateIDError")

  def build_id_registry(self):
    if self.items:
      for tree_branch in self.items:
        ids_to_append = []

        if self.check_for_duplicates(tree_branch['id']):
          ids_to_append.append(tree_branch['id'])

        if tree_branch.has_key('children'):
          children = tree_branch['children']
          for child in children:
            if self.check_for_duplicates(child['id']):
              ids_to_append.append(child['id'])

        for i in ids_to_append:
          self.id_registry.append(i)

    else:
      raise Exception("NoItemsInTree: Cannot Check empty tree")


  def add_child_node(self,attrs):
      if not isinstance(attrs,DijitTreeNode):
        raise Exception("Not a DijitTreeNode Instance")
      else:
        node = attrs.node
        branch_id = node['id']
        id_list = [node['id']]

        if node.has_key('children'):
          children = node['children']
          for child in children:
            id_list.append(child['id'])

        for i in id_list:
          if self.check_for_duplicates(i):
            self.id_registry.append(i)
            continue
          else:
            raise Exception("DuplicateIDError")
        self.items.append(node)


  def __unicode__(self):
    return unicode(self.node)

  def __repr__(self):
    if self.node:
      return str(self.node)
    else:
      return "__repr__ function returning the self.node attribute"

  def __call__(self):
    return self.node

  def to_json(self):
    return json.dumps(self.node)



################################################################################






    #if self.check_node_attr(attrs):
      #self.node = attrs
      #for k,v in attrs.iteritems():
        #if k == 'id' and not self.id_registry.has_key(v):
          #self.id_registry[v] = self.node
    #else:
      #raise Exception("InvalidInstantiationAttributes")

  #def __setitem__(self,key,value):
    #if self.node:
        #old_val = self.__getitem__(key)
        #self.node[key] = value
        #if key =='id':
          #self.id_registry.pop(old_val)
          #self.id_registry[value] = self.node
    #else:
      #raise Exception("Node has not been set")

  
  #def __getitem__(self,index):
    #if self.node:
      #try:
        #return self.node[index]
      #except KeyError:
        #raise KeyError
  

  ##def set(self,key,value):
    ##return self.__setitem__(key,value)

  ##def get(self,index):
    ##return self.__getitem__(index)

  #def get_item_by_id(self,node_id):
    #return self.id_registry.get(node_id)

  #def check_node_attr(self, attrs):
    #if isinstance(attrs,DijitTreeNode):
      #attrs = attrs.node

    #for attr in self.basic_node_attrs:
      #if attrs[attr]:
        #continue
      #else:
        #return False
    #return True
  
  #def check_branch_attr(self, attrs):
    #if isinstance(attrs,DijitTreeNode):
      #attrs = attrs.node
    #for attr in self.basic_branch_attrs:
      #if attrs[attr]:
        #continue
      #else:
        #return False
    #return True

  #def is_id_unique(self,attrs):
    #id_val = attrs['id']
    #if self.id_registry.has_key(id_val):
      #raise Exception("DuplicateIDError")
    #else:
      #if self.node.has_key('items'):
        #items = self.node['items']
        #if items:
          #for item in items:
            #if item.has_key('children'):
              #children = item['children']
              #if children:
                #for child in children:
                  #if child['id'] == id_val:
                    #raise Exception("DuplicateIDError")
                  #else:
                    #continue
      #return True

  #def get_child_node_by_id(self,branch_id):
    #if self.branch_dict.has_key(branch_id):
      #return self.branch_dict[branch_id]
    #else:
      #return None

  #def add_child_node(self,attrs):
    #if self.check_branch_attr(attrs) and self.is_id_unique(attrs):
      #attr_id = attrs['id']

      #if not self.node.has_key('items'):
        #self.node['items'] = [] 

      #if not isinstance(attrs,DijitTreeNode):
        #self.branch_dict[attr_id] = DijitTreeNode(attrs)
        #self.node['items'].append(attrs)
      #else:
        #self.branch_dict[attr_id] = attrs
        #self.node['items'].append(attrs.node)

    #else:
      #raise AttributeError

  #def update_child_node(self,branch_id,attrs):
    #branch = self.get_child_node_by_id(branch_id)
    #if branch:
      #attr_id = attrs['id']
      #if self.check_branch_attr(attrs) and attr_id != branch_id:
          #if self.is_id_unique(attrs):
            #self.branch_dict.pop(branch_id)
            #if not isinstance(attrs,DijitTreeNode):
              #self.branch_dict[attr_id]= DijitTreeNode(attrs)
            #else:
              #self.branch_dict[attr_id] = attrs
            ##if not self.node.has_key('items'):
              ##self.node['items'] = []
            ##self.node['items'] = self.branch_dict.values()
          #else:
            #raise Exception("DuplicateIDError: While updating")
      #else:
        #raise Exception("InvalidBranchAttributes")
    #else:
      #raise Exception("InvalidBranchId")


  #def del_child_node(self,branch_id):
    #branch = self.get_child_node_by_id(branch_id)
    #if branch:
      #self.branch_dict.pop(branch_id)
    #else:
      #raise Exception("InvalidBranchId")
