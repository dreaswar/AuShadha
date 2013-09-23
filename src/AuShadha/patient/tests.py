"""This file demonstrates writing tests using the unittest module. These will
pass when you run "manage.py test".

Replace this with more appropriate tests for your application.

"""

from django.test import TestCase
from django.utils import simplejson

class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class DijitTree(object):

  tree = {}
  trunk = {'identifier':'','label':''}
  id_registry = []

  basic_branch_attrs = ['name','type','id']
  extra_branch_attrs = ['len','addUrl','children']

  def __init__(self,
               identifier = 'id',
               label='name',
               items = [{'name':'History','type':'module'},
                        {'name':'Investigation','type':'module','id':'INV'},
                        {'name':'Imaging','type':'module','id':'IMAGING'},
                        {'name':'Procedure','type':'module','id':'PROCEDURES'},
                        {'name':'Visit','type':'module','id':'VISIT'},
                        {'name':'Admission','type':'module','id':'ADMISSION'},
                        {'name':'Immunisation','type':'module','id':'IMMUNISATION'},
                        {'name':'Coding','type':'module','id':'CODING'}
                        ]):

    self.identifier = unicode(identifier)
    self.label = unicode(label)
    self.trunk['identifier'] = self.identifier
    self.trunk['label'] = self.label,
    
    if items and type(items) is list :

      for branch_node in items:
        print "checking, ", branch_node

        if self.check_branch_attr(branch_node):
          branch_id = branch_node.get('id')
          if branch_id and branch_id not in self.id_registry:
            self.id_registry.append(branch_id)
            print "Appended id to registry"
          else:
            raise Exception("DuplicateIDError with:%s" %(branch_id) )

        else:
            raise Exception("BasicAttrNotSupplied with branch")

      self.branches = items
      self.merge_branches_to_trunk()
      self.create_tree()

    elif not items:
          raise Exception("NoItemsListed. Cannot Initialize Branchless Tree")
    else:
      raise TypeError("Items to the Tree has to be a list")


  def __call__(self):
    return self.tree

  def __unicode__(self):
    return self.__call__()

  def check_branch_attr(self, node):
    keys = node.keys()
    basic_attrs = self.basic_branch_attrs
    for i in basic_attrs:
      print "Checking for ", i, " in ", keys
      if i in keys:
        continue
      else:
        raise Exception("RequiredKeyNotSupplied in branch")
    return True

  def create_tree(self):
    self.tree = simplejson.dumps(self.trunk)
    print "Finished creating Tree"    


  def merge_branches_to_trunk(self):
    self.trunk['items'] = self.branches
    print "Finished merging branches"

  def add_branch(node_to_append,branch_obj):
    pass
  
  def edit_branch(branch_to_edit):
    pass

  def remove_branch(branch_to_remove):
    pass

  

class DijitTreeRoot(object):
  pass

class DijitTreeTrunk(object):
  pass

class DijitTreeBranch(object):
  branch_attrs = {'name':'','type':'','id':'','len':'','addUrl':'','children':[]}
  pass

class DijitTreeSubBranch(object):
  pass
