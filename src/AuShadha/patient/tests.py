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


DIJIT_TREE_LIST = [ 
                    {'name':'History','type':'module','id':"HISTORY"},
                    {'name':'Investigation','type':'module','id':'INV'},
                    {'name':'Imaging','type':'module','id':'IMAGING'},
                    {'name':'Procedure','type':'module','id':'PROCEDURES'},
                    {'name':'Visit','type':'module','id':'VISIT'},
                    {'name':'Admission','type':'module','id':'ADMISSION'},
                    {'name':'Immunisation','type':'module','id':'IMMUNISATION'},
                    {'name':'Coding','type':'module','id':'CODING'}
                  ]