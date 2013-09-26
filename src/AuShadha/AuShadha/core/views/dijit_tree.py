################################################################################
# Project     : AuShadha
# Description : Constructing a Dijit Tree  
# Author      : Dr. Easwar T.R
# Date        : 25-09-2013
# License     : GNU-GPL Version 3 , See AuShadha/LICENSE.txt
################################################################################

import json as JSON
#from django.utils import simplejson
#from django.core import serializers
#from django.core.serializers import json
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
        print "Setting ", k , " as pointing to ",v
        self.k = v
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
    print "Type of node is : ", type(self.node)
    return self.node
    #return JSON.dumps( self.node ,encoding = 'UTF-8',default = str)

  def to_json(self):
    node = self.node
    #for k, v in node.iteritems():
      #if not type(v) is list:
        #print type(k), "--> " , k, "::--> ",v, type(v)
      #else:
        #for item in v:
          #print item, type(item)
    print "Trying to serialize node of type ", type(self.node)
    return JSON.dumps(node)

  #def set(self,key,value):
    #return self.__setitem__(key,value)

  #def get(self,index):
    #return self.__getitem__(index)

  def get_item_by_id(self,node_id):
    return self.id_registry.get(node_id)

  def check_node_attr(self, attrs):
    for attr in self.basic_node_attrs:
      print "Checking for attr: ",attr, " in self.basic_node_attrs"
      if attrs[attr]:
        print "Attribute: ", attr, " is present "
        continue
      else:
        print "Attribute: ", attr, " is not present "
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
  
  def __init__(self,attrs = {'identifier':'id','label':'name','items':[]}):

    self.basic_node_attrs = ['identifier','label']
    self.basic_branch_attrs = ['id','name','type']
    self.extra_branch_attrs = ['addUrl','children','len']
    self.branch_dict = {}
    self.id_registry={}

    if self.check_node_attr(attrs):
      self.node = attrs
      for k,v in attrs.iteritems():
        print "Setting ", k , " as pointing to ",v
        self.k = v
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
    node = self.node
    print "Trying to serialize node of type ", type(self.node)
    return JSON.dumps(node)

  #def set(self,key,value):
    #return self.__setitem__(key,value)

  #def get(self,index):
    #return self.__getitem__(index)

  def get_item_by_id(self,node_id):
    return self.id_registry.get(node_id)

  def check_node_attr(self, attrs):
    if isinstance(attrs,DijitTreeNode):
      attrs = attrs.node

    for attr in self.basic_node_attrs:
      print "Checking for attr: ",attr, " in self.basic_node_attrs"
      if attrs[attr]:
        print "Attribute: ", attr, " is present "
        continue
      else:
        print "Attribute: ", attr, " is not present "
        return False
    return True
  
  def check_branch_attr(self, attrs):
    if isinstance(attrs,DijitTreeNode):
      attrs = attrs.node
    for attr in self.basic_branch_attrs:
      print "Checking for attr: ",attr, " in self.basic_node_attrs"
      if attrs[attr]:
        print "Attribute: ", attr, " is present "
        continue
      else:
        print "Attribute: ", attr, " is not present "
        return False
    return True

  def is_id_unique(self,attrs):
    id_val = attrs['id']
    if self.id_registry.has_key(id_val):
      raise Exception("DuplicateIDError")
    else:
      if self.node.has_key('items'):
        items = self.node['items']
        if items:
          print "Items are: "
          print items
          for item in items:
            if item.has_key('children'):
              children = item['children']
              if children:
                for child in children:
                  if child['id'] == id_val:
                    raise Exception("DuplicateIDError")
                  else:
                    continue
      return True

  def get_child_node_by_id(self,branch_id):
    if self.branch_dict.has_key(branch_id):
      return self.branch_dict[branch_id]
    else:
      return None

  def add_child_node(self,attrs):
    if self.check_branch_attr(attrs) and self.is_id_unique(attrs):
      attr_id = attrs['id']

      if not self.node.has_key('items'):
        items = self.node['items'] = [] 
      else:
        items = self.node['items']

      if not isinstance(attrs,DijitTreeNode):
        self.branch_dict[attr_id] = DijitTreeNode(attrs)
        items.append(attrs)
      else:
        self.branch_dict[attr_id] = attrs
        items.append(attrs.node)

    else:
      raise AttributeError

  def update_child_node(self,branch_id,attrs):
    branch = self.get_child_node_by_id(branch_id)
    if branch:
      attr_id = attrs['id']
      if self.check_branch_attr(attrs) and attr_id != branch_id:
          if self.is_id_unique(attrs):
            self.branch_dict.pop(branch_id)
            if not isinstance(attrs,DijitTreeNode):
              self.branch_dict[attr_id]= DijitTreeNode(attrs)
            else:
              self.branch_dict[attr_id] = attrs
            #if not self.node.has_key('items'):
              #self.node['items'] = []
            #self.node['items'] = self.branch_dict.values()
          else:
            raise Exception("DuplicateIDError: While updating")
      else:
        raise Exception("InvalidBranchAttributes")
    else:
      raise Exception("InvalidBranchId")


  def del_child_node(self,branch_id):
    branch = self.get_child_node_by_id(branch_id)
    if branch:
      self.branch_dict.pop(branch_id)
    else:
      raise Exception("InvalidBranchId")
