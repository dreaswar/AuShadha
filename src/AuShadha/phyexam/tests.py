"""This file demonstrates writing tests using the unittest module. These will
pass when you run "manage.py test".

Replace this with more appropriate tests for your application.

"""

from django.test import TestCase

import datetime

from patient.models import PatientDetail
from clinic.models import Clinic, Staff
from visit.models import VisitDetail
from phyexam.models import PhyExamBaseModel



class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class TestUrlsForPhyExam(object):
  
  def __init__(self):
    self.pat= PatientDetail.objects.get(pk =1)
    self.surg = Staff.objects.get(pk = 1)
    self.clinic = Clinic.objects.get(pk = 1)


  def __call__(self):
    self.vis = VisitDetail()
    self.vis.patient_detail = self.pat
    self.vis.visit_date = datetime.datetime.now()
    self.vis.op_surgeon = self.surg
    self.vis.save()

    self.pat.save()

    print "URLS for Patient is " 
    print self.pat.urls
    print "#"*30

    print "URLS for Visit is " 
    print self.vis.urls
    print "#"*30


    self.pe = PhyExamBaseModel(visit_detail = self.vis,physician = self.surg)
    self.pe.save()

    print "URLS for Phyexam is" 
    print self.pe.urls
    print "#"*30

t = TestUrlsForPhyExam()
t()